import os
import sounddevice as sd
import numpy as np
import soundfile as sf
from scipy.io.wavfile import write
from datetime import datetime
from PySide6.QtWidgets import (
    QDialog, QFileDialog, QMessageBox, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QGroupBox,
    QSizePolicy, QFrame
)
from PySide6.QtCore import QTimer, QThread, Signal, Qt
from PySide6.QtGui import QPainter, QColor, QPen
from gui.analysis import Ui_AnalysisDialog
from core.voice_analysis_service import VoiceAnalysisService
import threading


# ─────────────────────────────────────────────
#  Виджет визуализации звуковой волны
# ─────────────────────────────────────────────
class WaveformWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.waveform_data = None
        self.playback_progress = 0.0
        self.setMinimumHeight(80)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet("background-color: #1a2332; border-radius: 8px;")

    def set_waveform(self, audio_data: np.ndarray):
        if audio_data.ndim > 1:
            audio_data = audio_data.mean(axis=1)
        num_points = 400
        step = max(1, len(audio_data) // num_points)
        sampled = audio_data[::step][:num_points]
        max_val = np.max(np.abs(sampled)) + 1e-8
        self.waveform_data = sampled / max_val
        self.update()

    def set_progress(self, progress: float):
        self.playback_progress = max(0.0, min(1.0, progress))
        self.update()

    def clear(self):
        self.waveform_data = None
        self.playback_progress = 0.0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        painter.fillRect(0, 0, w, h, QColor("#1a2332"))

        if self.waveform_data is None:
            pen = QPen(QColor("#3a4a5c"), 1, Qt.DashLine)
            painter.setPen(pen)
            painter.drawLine(0, h // 2, w, h // 2)
            painter.setPen(QColor("#5a6a7c"))
            painter.drawText(0, 0, w, h, Qt.AlignCenter, "Загрузите аудио для отображения волны")
            painter.end()
            return

        num_points = len(self.waveform_data)
        bar_width = max(1, w // num_points)
        played_x = int(w * self.playback_progress)

        for i, val in enumerate(self.waveform_data):
            x = int(i * w / num_points)
            bar_h = max(2, int(abs(val) * (h // 2 - 6)))
            color = QColor("#3498DB") if x <= played_x else QColor("#2c3e50")
            painter.fillRect(x, h // 2 - bar_h, bar_width, bar_h * 2, color)

        if self.playback_progress > 0:
            pen = QPen(QColor("#ffffff"), 2)
            painter.setPen(pen)
            painter.drawLine(played_x, 4, played_x, h - 4)

        painter.end()


# ─────────────────────────────────────────────
#  Основной контроллер анализа
# ─────────────────────────────────────────────
class AnalysisController:
    def __init__(self, main):
        self.main = main
        self.current_audio_file = None
        self.is_playing = False
        self.is_recording = False
        self.audio_data = None
        self.sample_rate = 44100
        self.current_sample = 0
        self.stream = None
        self.play_timer = None
        self.record_sample_rate = 44100
        self.recorded_chunks = []
        self.recording_thread = None
        self.output_dir = "records"
        self.recent_files = []
        self.recent_files_path = "data/recent_files.json"
        os.makedirs(self.output_dir, exist_ok=True)

        self._setup_analysis_page_ui()

    def _setup_analysis_page_ui(self):
        """Программно добавляет виджеты на page_analysis"""
        page = self.main.page_analysis

        # ── Метки времени — снаружи groupBox, прямо под ним ──
        time_frame = QFrame(page)
        time_frame.setGeometry(10, 222, 601, 20)
        time_frame.setStyleSheet("background: transparent; border: none;")
        time_layout = QHBoxLayout(time_frame)
        time_layout.setContentsMargins(4, 0, 4, 0)

        self.label_time_current = QLabel("0:00")
        self.label_time_current.setStyleSheet("color: #3498DB; font-weight: bold; font-size: 11px;")
        self.label_time_total = QLabel("0:00")
        self.label_time_total.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        self.label_time_total.setAlignment(Qt.AlignRight)
        time_layout.addWidget(self.label_time_current)
        time_layout.addStretch()
        time_layout.addWidget(self.label_time_total)

        # ── Улучшаем кнопки плеера ──
        self.main.btn_start_audio.setText("▶ ")
        self.main.btn_pause_audio.setText("| |")
        self.main.btn_close_audio.setText("✕")

        # ── Карточка метаданных файла ──
        self.card_frame = QFrame(page)
        self.card_frame.setGeometry(10, 248, 601, 38)
        self.card_frame.setStyleSheet("""
            QFrame {
                background-color: #EBF5FB;
                border: 1px solid #AED6F1;
                border-radius: 6px;
            }
        """)
        card_layout = QHBoxLayout(self.card_frame)
        card_layout.setContentsMargins(10, 4, 10, 4)
        card_layout.setSpacing(20)

        self.label_file_format = QLabel("Формат: —")
        self.label_file_duration = QLabel("⏱ —")
        self.label_file_size = QLabel("💾 —")
        self.label_file_sr = QLabel("📡 —")

        for lbl in [self.label_file_format, self.label_file_duration,
                    self.label_file_size, self.label_file_sr]:
            lbl.setStyleSheet("color: #1A5276; font-size: 11px; font-weight: bold;")
            card_layout.addWidget(lbl)

        self.card_frame.hide()

        # ── Визуализация волны ──
        self.waveform_widget = WaveformWidget(page)
        self.waveform_widget.setGeometry(10, 294, 601, 88)

        # ── Список последних файлов ──
        group_recent = QGroupBox("🕒  Последние файлы", page)
        group_recent.setGeometry(10, 390, 601, 90)
        group_recent.setStyleSheet("""
            QGroupBox {
                font-weight: bold; font-size: 12px;
                border: 1px solid #BDC3C7; border-radius: 5px;
                margin-top: 8px; padding-top: 8px;
                color: #2C3E50; background-color: white;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
        """)
        recent_layout = QVBoxLayout(group_recent)
        recent_layout.setContentsMargins(6, 14, 6, 4)

        self.list_recent_files = QListWidget()
        self.list_recent_files.setFixedHeight(58)
        self.list_recent_files.setStyleSheet("""
            QListWidget {
                border: none; background: transparent;
                font-size: 12px; color: #2C3E50;
            }
            QListWidget::item { padding: 2px 4px; border-radius: 3px; }
            QListWidget::item:hover { background-color: #EBF5FB; color: #1A5276; }
            QListWidget::item:selected { background-color: #3498DB; color: white; }
        """)
        self.list_recent_files.itemDoubleClicked.connect(self._load_recent_file)
        recent_layout.addWidget(self.list_recent_files)

    def setup_connections(self):
        self.main.btn_record_audio.clicked.connect(self.toggle_recording)
        self.main.btn_analysis_audio.clicked.connect(self.open_analysis_window)
        self.main.btn_load_audio.clicked.connect(self.load_audio)
        self.main.btn_start_audio.clicked.connect(self.start_audio)
        self.main.btn_pause_audio.clicked.connect(self.pause_audio)
        self.main.btn_close_audio.clicked.connect(self.close_audio)

        # Загружаем последние файлы с диска
        self._load_recent_from_disk()

    # ─── Запись ───────────────────────────────

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.is_recording = True
        self.recorded_chunks = []
        self.main.btn_record_audio.setText("Остановить запись")
        self.main.btn_record_audio.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C; color: white; border: none;
                padding: 8px 12px; border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #C0392B; }
        """)
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.start()

    def _record_audio(self):
        with sd.InputStream(samplerate=self.record_sample_rate, channels=1, callback=self._callback):
            while self.is_recording:
                sd.sleep(100)

    def _callback(self, indata, frames, time, status):
        if status:
            print("Status:", status)
        self.recorded_chunks.append(indata.copy())

    def stop_recording(self):
        self.is_recording = False
        if self.recording_thread is not None:
            self.recording_thread.join()

        self.main.btn_record_audio.setText("Записать аудио")
        self.main.btn_record_audio.setStyleSheet("""
            QPushButton {
                background-color: #3498DB; color: white; border: none;
                padding: 8px 12px; border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #2980B9; padding-left: 14px; }
        """)

        if not self.recorded_chunks:
            return

        audio_np = np.concatenate(self.recorded_chunks, axis=0)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(self.output_dir, f"record_{timestamp}.wav")
        write(filename, self.record_sample_rate, (audio_np * 32767).astype(np.int16))
        self._load_file(filename)

    # ─── Загрузка файла ───────────────────────

    def load_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.main, "Выберите аудио файл", "",
            "Аудио файлы (*.wav *.mp3 *.flac);;Все файлы (*)"
        )
        if file_path:
            self._load_file(file_path)

    def _load_file(self, file_path: str):
        try:
            self.current_audio_file = file_path
            self.audio_data, self.sample_rate = sf.read(file_path)
            if self.audio_data.ndim == 1:
                self.audio_data = self.audio_data.reshape(-1, 1)
            self.current_sample = 0

            self.main.label_file_name.setText(f"{os.path.basename(file_path)}")
            self.main.progress_audio.setValue(0)

            self._update_file_card(file_path)
            self.waveform_widget.set_waveform(self.audio_data)
            self.waveform_widget.set_progress(0.0)
            self._add_to_recent(file_path)

            total_sec = len(self.audio_data) / self.sample_rate
            self.label_time_total.setText(self._fmt_time(total_sec))
            self.label_time_current.setText("0:00")

            self.main.btn_start_audio.setEnabled(True)
            self.main.btn_pause_audio.setEnabled(True)
            self.main.btn_close_audio.setEnabled(True)

        except Exception as e:
            self.main.label_file_name.setText("Ошибка: неподдерживаемый формат")
            print(f"Ошибка загрузки: {e}")

    def _update_file_card(self, file_path: str):
        try:
            ext = os.path.splitext(file_path)[1].upper().lstrip(".")
            size_kb = os.path.getsize(file_path) / 1024
            size_str = f"{size_kb:.1f} КБ" if size_kb < 1024 else f"{size_kb/1024:.1f} МБ"
            duration_sec = len(self.audio_data) / self.sample_rate

            self.label_file_format.setText(f"Формат: {ext}")
            self.label_file_duration.setText(f"⏱ {self._fmt_time(duration_sec)}")
            self.label_file_size.setText(f"💾 {size_str}")
            self.label_file_sr.setText(f"📡 {self.sample_rate} Гц")
            self.card_frame.show()
        except Exception as e:
            print(f"Ошибка карточки: {e}")

    def _add_to_recent(self, file_path: str):
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        self.recent_files = self.recent_files[:2]
        self._save_recent_to_disk()
        self._refresh_recent_list()

    def _refresh_recent_list(self):
        self.list_recent_files.clear()
        for fp in self.recent_files:
            item = QListWidgetItem(f"  📄 {os.path.basename(fp)}")
            item.setData(Qt.UserRole, fp)
            item.setToolTip(fp)
            self.list_recent_files.addItem(item)

    def _save_recent_to_disk(self):
        try:
            import json
            os.makedirs(os.path.dirname(self.recent_files_path), exist_ok=True)
            with open(self.recent_files_path, "w", encoding="utf-8") as f:
                json.dump(self.recent_files, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения recent файлов: {e}")

    def _load_recent_from_disk(self):
        try:
            import json
            if os.path.exists(self.recent_files_path):
                with open(self.recent_files_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                # Оставляем только существующие файлы
                self.recent_files = [f for f in loaded if os.path.exists(f)][:5]
                self._refresh_recent_list()
        except Exception as e:
            print(f"Ошибка загрузки recent файлов: {e}")

    def _load_recent_file(self, item: QListWidgetItem):
        path = item.data(Qt.UserRole)
        if path and os.path.exists(path):
            self._load_file(path)
        else:
            QMessageBox.warning(self.main, "Файл не найден", f"Файл не существует:\n{path}")

    # ─── Воспроизведение ──────────────────────

    def start_audio(self):
        if not self.current_audio_file or self.audio_data is None:
            return
        if not self.is_playing:
            if self.current_sample >= len(self.audio_data):
                self.current_sample = 0
            self.is_playing = True
            self.stream = sd.OutputStream(
                samplerate=self.sample_rate,
                channels=self.audio_data.shape[1],
                callback=self.audio_callback
            )
            self.stream.start()
            self.play_timer = QTimer()
            self.play_timer.timeout.connect(self.update_play_progress)
            self.play_timer.start(50)

    def audio_callback(self, outdata, frames, time, status):
        end_sample = self.current_sample + frames
        if end_sample >= len(self.audio_data):
            end_sample = len(self.audio_data)
            outdata[:end_sample - self.current_sample] = self.audio_data[self.current_sample:end_sample]
            outdata[end_sample - self.current_sample:] = 0
            self.current_sample = end_sample
            raise sd.CallbackStop
        else:
            outdata[:] = self.audio_data[self.current_sample:end_sample]
            self.current_sample = end_sample

    def update_play_progress(self):
        if self.is_playing and self.audio_data is not None:
            progress = self.current_sample / len(self.audio_data)
            self.main.progress_audio.setValue(int(min(progress * 100, 100.0)))
            self.waveform_widget.set_progress(progress)
            self.label_time_current.setText(self._fmt_time(self.current_sample / self.sample_rate))

            if self.current_sample >= len(self.audio_data):
                self.stop_audio()
                self.main.progress_audio.setValue(100)
                self.waveform_widget.set_progress(1.0)

    def pause_audio(self):
        if self.is_playing:
            self.is_playing = False
            if self.stream:
                self.stream.stop()
            if self.play_timer:
                self.play_timer.stop()
                self.play_timer = None

    def close_audio(self):
        self.stop_audio()
        self.current_sample = 0
        self.audio_data = None
        self.sample_rate = 0
        self.current_audio_file = None
        self.main.progress_audio.setValue(0)
        self.main.label_file_name.setText("Файл не выбран")
        self.label_time_current.setText("0:00")
        self.label_time_total.setText("0:00")
        self.waveform_widget.clear()
        self.card_frame.hide()
        self.main.btn_start_audio.setEnabled(False)
        self.main.btn_pause_audio.setEnabled(False)
        self.main.btn_close_audio.setEnabled(False)

    def stop_audio(self):
        self.is_playing = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        if self.play_timer:
            self.play_timer.stop()
            self.play_timer = None

    def open_analysis_window(self):
        if not self.current_audio_file:
            QMessageBox.warning(self.main, "Внимание!", "Сначала загрузите или запишите аудио файл!")
            return
        analysis_window = AnalysisWindow(self.main, self.current_audio_file)
        analysis_window.exec()

    @staticmethod
    def _fmt_time(seconds: float) -> str:
        m = int(seconds) // 60
        s = int(seconds) % 60
        return f"{m}:{s:02d}"


# ─────────────────────────────────────────────
#  Поток анализа и окно результатов
# ─────────────────────────────────────────────
class AnalysisThread(QThread):
    finished_signal = Signal(dict)

    def __init__(self, audio_file):
        super().__init__()
        self.audio_file = audio_file
        self.analyzer = VoiceAnalysisService()

    def run(self):
        try:
            result = self.analyzer.analyze(self.audio_file)
        except Exception as e:
            result = {"status": "error", "message": str(e)}
        self.finished_signal.emit(result)


class AnalysisWindow(QDialog, Ui_AnalysisDialog):
    def __init__(self, parent=None, audio_file=None):
        super().__init__(parent)
        self.setupUi(self)
        self.audio_file = audio_file
        self.setWindowTitle("Анализ аудио")
        self.setFixedSize(700, 519)
        self.btn_close.clicked.connect(self.close)
        self.btn_save.setEnabled(False)

        if not audio_file:
            return

        self.label_status.setText(f"Анализ файла: {audio_file.split('/')[-1]}")
        self.textEdit_results.setText("⏳ Извлекаются голосовые признаки...")

        self.thread = AnalysisThread(audio_file)
        self.thread.finished_signal.connect(self.show_result)
        self.thread.start()

    def show_result(self, result):
        if result["status"] == "ok":
            text = "🎤 Анализ завершён\n"
            text += f"👤 Найден голос: {result['best_match']['person']['full_name']}\n"
            text += f"📊 Сходство: {result['best_match']['similarity'] * 100:.1f}%\n"
            text += f"📈 Уверенность: {result['best_match']['confidence']}\n"
            text += f"🧩 Сегментов проанализировано: {result['segments']}\n"
            text += f"⏱ Время анализа: {result['analysis_time']} сек\n\n"
            text += "🔍 Другие совпадения:\n"
            for i, (name, score) in enumerate(result["top_matches"], 1):
                icon = "✅" if score >= 0.7 else "⚠️" if score >= 0.6 else "❌"
                text += f"{i}. {icon} {name}: {score * 100:.1f}%\n"
            self.textEdit_results.setText(text)
            self.btn_save.setEnabled(True)

        elif result["status"] == "not_found":
            text = "❌ Голос не найден в базе.\n\n"
            text += f"Проанализировано сегментов: {result['segments']}\n"
            text += f"Время анализа: {result['analysis_time']} сек\n\n"
            text += "Возможные причины:\n1. Человек отсутствует в базе\n"
            text += "2. Аудио слишком короткое\n3. Сильный фоновый шум\n4. Низкое качество записи"
            self.textEdit_results.setText(text)
        else:
            self.textEdit_results.setText(
                f"❌ Ошибка анализа: {result.get('message', 'Неизвестная ошибка')}"
            )