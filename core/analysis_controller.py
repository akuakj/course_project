import os
import numpy as np
import soundfile as sf
import sounddevice as sd
from scipy.io.wavfile import write
from datetime import datetime
from PySide6.QtWidgets import (
    QDialog, QFileDialog, QMessageBox, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QGroupBox,
    QSizePolicy, QFrame, QProgressBar, QScrollArea, QPushButton
)
from PySide6.QtCore import QTimer, QThread, Signal, Qt
from PySide6.QtGui import QPainter, QColor, QPen, QPixmap, QFont
from core.voice_analysis_service import VoiceAnalysisService
import threading
from core.db_manager import TinyDBVoiceManager
from core.person_details_dialog import PersonDetailsDialog
from core.database_controller import DatabaseController

#  Виджет визуализации звуковой волны
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


#  Основной контроллер анализа
class AnalysisController:
    def __init__(self, main):
        self.main = main
        self.db_manager = main.db_manager
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
        page = self.main.page_analysis

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

        self.main.btn_start_audio.setText("▶ ")
        self.main.btn_pause_audio.setText("| |")
        self.main.btn_close_audio.setText("✕")

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

        self.waveform_widget = WaveformWidget(page)
        self.waveform_widget.setGeometry(10, 294, 601, 88)

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
        self._load_recent_from_disk()

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
            self.recording_thread.join(timeout=3)
            self.recording_thread = None

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
                self.recent_files = [f for f in loaded if os.path.exists(f)][:2]
                self._refresh_recent_list()
        except Exception as e:
            print(f"Ошибка загрузки recent файлов: {e}")

    def _load_recent_file(self, item: QListWidgetItem):
        path = item.data(Qt.UserRole)
        if path and os.path.exists(path):
            self._load_file(path)
        else:
            QMessageBox.warning(self.main, "Файл не найден", f"Файл не существует:\n{path}")

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
        analysis_window = AnalysisWindow(self.main, self.current_audio_file, db_manager=self.main.db_manager)
        analysis_window.exec()

    @staticmethod
    def _fmt_time(seconds: float) -> str:
        m = int(seconds) // 60
        s = int(seconds) % 60
        return f"{m}:{s:02d}"


#  Поток анализа
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



#  Окно результатов анализа
class AnalysisWindow(QDialog):
    def __init__(self, parent=None, audio_file=None, db_manager=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.audio_file = audio_file
        self.thread = None
        self.setWindowTitle("Анализ аудио")
        self.setFixedSize(720, 560)
        self.setStyleSheet("""
            QDialog { background-color: #F0F4F8; }
            QScrollBar:vertical {
                background: transparent; width: 6px; margin: 4px 2px; border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: #CBD5E1; border-radius: 3px; min-height: 30px;
            }
            QScrollBar::handle:vertical:hover { background: #94A3B8; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
        """)

        def closeEvent(self, event):
            if self.thread and self.thread.isRunning():
                self.thread.quit()
                self.thread.wait(3000)
            event.accept()

        self._init_ui()

        if audio_file:
            self._start_analysis()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ШАПКА
        header = QFrame()
        header.setFixedHeight(64)
        header.setStyleSheet("QFrame { background-color: #1a1f2e; border: none; }")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)

        title = QLabel("Анализ голоса")
        title.setStyleSheet("color: white; font-size: 15px; font-weight: bold; background: transparent;")

        self.filename_badge = QLabel(os.path.basename(self.audio_file) if self.audio_file else "")
        self.filename_badge.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)

        self.filename_badge.setStyleSheet("""
            QLabel {
                background-color: rgba(52,152,219,0.2);
                color: #3498db;
                border: 1px solid #3498db;
                border-radius: 10px;
                font-size: 11px;
                font-weight: bold;
                padding: 3px 10px;
            }
        """)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.filename_badge)
        main_layout.addWidget(header)

        # ПРОГРЕСС БАР
        self.progress_frame = QFrame()
        self.progress_frame.setFixedHeight(36)
        self.progress_frame.setStyleSheet("QFrame { background: white; border: none; border-bottom: 1px solid #E2E8F0; }")
        progress_layout = QHBoxLayout(self.progress_frame)
        progress_layout.setContentsMargins(20, 6, 20, 6)

        self.status_label = QLabel("Извлечение голосовых признаков...")
        self.status_label.setStyleSheet("color: #64748B; font-size: 12px; background: transparent;")

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 0)  # бесконечный пока идёт анализ
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none; border-radius: 3px; background: #E2E8F0;
            }
            QProgressBar::chunk {
                background: #3B82F6; border-radius: 3px;
            }
        """)

        progress_layout.addWidget(self.status_label)
        progress_layout.addStretch()
        progress_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.progress_frame)

        # ТЕЛО
        body = QWidget()
        body.setStyleSheet("background: #F0F4F8;")
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(16, 16, 16, 16)
        body_layout.setSpacing(14)

        # ЛЕВАЯ ЧАСТЬ — спектрограмма
        left = QVBoxLayout()
        left.setSpacing(10)

        spec_card = QFrame()
        spec_card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 10px;
                border: 1px solid #E2E8F0;
            }
        """)
        spec_layout = QVBoxLayout(spec_card)
        spec_layout.setContentsMargins(14, 12, 14, 12)
        spec_layout.setSpacing(8)

        spec_header = QLabel("СПЕКТРОГРАММА")
        spec_header.setStyleSheet("""
            QLabel {
                color: #94A3B8; font-size: 10px; font-weight: bold;
                letter-spacing: 1px; background: transparent; border: none;
            }
        """)
        spec_layout.addWidget(spec_header)

        self.spec_label = QLabel()
        self.spec_label.setFixedSize(330, 190)
        self.spec_label.setAlignment(Qt.AlignCenter)
        self.spec_label.setStyleSheet("""
            QLabel {
                background: #0F172A;
                border-radius: 8px;
                color: #475569;
                font-size: 12px;
                border: none;
            }
        """)
        self.spec_label.setText("Строится спектрограмма...")
        spec_layout.addWidget(self.spec_label)
        left.addWidget(spec_card)
        left.addStretch()

        body_layout.addLayout(left)

        # ПРАВАЯ ЧАСТЬ — результаты
        right = QVBoxLayout()
        right.setSpacing(10)

        # Карточка главного результата
        self.result_card = QFrame()
        self.result_card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 10px;
                border: 1px solid #E2E8F0;
            }
        """)
        result_layout = QVBoxLayout(self.result_card)
        result_layout.setContentsMargins(16, 14, 16, 14)
        result_layout.setSpacing(6)

        res_header = QLabel("РЕЗУЛЬТАТ")
        res_header.setStyleSheet("color: #94A3B8; font-size: 10px; font-weight: bold; letter-spacing: 1px; background: transparent; border: none;")
        result_layout.addWidget(res_header)

        self.result_name = QLabel("Анализируется...")
        self.result_name.setStyleSheet("color: #1E293B; font-size: 18px; font-weight: bold; background: transparent; border: none;")
        result_layout.addWidget(self.result_name)

        self.result_meta = QLabel("")
        self.result_meta.setWordWrap(True)  # ← добавь эту строку
        self.result_meta.setStyleSheet("color: #64748B; font-size: 12px; background: transparent; border: none;")
        result_layout.addWidget(self.result_meta)

        right.addWidget(self.result_card)

        # Карточка совпадений
        matches_card = QFrame()
        matches_card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 10px;
                border: 1px solid #E2E8F0;
            }
        """)
        matches_layout = QVBoxLayout(matches_card)
        matches_layout.setContentsMargins(16, 12, 16, 12)
        matches_layout.setSpacing(8)

        matches_header = QLabel("ВСЕ СОВПАДЕНИЯ")
        matches_header.setStyleSheet("color: #94A3B8; font-size: 10px; font-weight: bold; letter-spacing: 1px; background: transparent; border: none;")
        matches_layout.addWidget(matches_header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        self.matches_widget = QWidget()
        self.matches_widget.setStyleSheet("background: transparent;")
        self.matches_inner = QVBoxLayout(self.matches_widget)
        self.matches_inner.setSpacing(6)
        self.matches_inner.setContentsMargins(0, 0, 0, 0)

        scroll.setWidget(self.matches_widget)
        matches_layout.addWidget(scroll)
        right.addWidget(matches_card)

        body_layout.addLayout(right)
        main_layout.addWidget(body)

        # ФУТЕР
        footer = QFrame()
        footer.setFixedHeight(58)
        footer.setStyleSheet("QFrame { background: white; border-top: 1px solid #E2E8F0; border: none; }")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(20, 0, 20, 0)

        self.time_label = QLabel("")
        self.time_label.setStyleSheet("color: #94A3B8; font-size: 11px;")

        close_btn = QPushButton("Закрыть")
        close_btn.setFixedSize(100, 36)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a1f2e; color: #94A3B8;
                border: none; border-radius: 6px;
                font-size: 12px; font-weight: bold;
            }
            QPushButton:hover { background-color: #2d3447; color: white; }
        """)

        footer_layout.addWidget(self.time_label)
        footer_layout.addStretch()
        footer_layout.addWidget(close_btn)
        main_layout.addWidget(footer)

    def _start_analysis(self):
        # Строим спектрограмму
        self._build_spectrogram()

        # Запускаем анализ в потоке
        self.thread = AnalysisThread(self.audio_file)
        self.thread.finished_signal.connect(self._show_result)
        self.thread.start()

    def _build_spectrogram(self):
        """Строит спектрограмму через matplotlib и вставляет как QPixmap"""
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            import matplotlib.colors as mcolors
            import io

            audio, sr = sf.read(self.audio_file)
            if audio.ndim > 1:
                audio = audio.mean(axis=1)

            fig, ax = plt.subplots(figsize=(3.2, 1.9), dpi=100)
            fig.patch.set_facecolor("#0F172A")
            ax.set_facecolor("#0F172A")

            ax.specgram(audio, Fs=sr, cmap="plasma", NFFT=512, noverlap=256)

            ax.set_xlabel("Время (с)", color="#64748B", fontsize=7)
            ax.set_ylabel("Частота (Гц)", color="#64748B", fontsize=7)
            ax.tick_params(colors="#475569", labelsize=6)
            for spine in ax.spines.values():
                spine.set_edgecolor("#1E293B")

            plt.tight_layout(pad=0.3)

            buf = io.BytesIO()
            plt.savefig(buf, format="png", facecolor=fig.get_facecolor())
            plt.close(fig)
            buf.seek(0)

            pixmap = QPixmap()
            pixmap.loadFromData(buf.read())
            self.spec_label.setPixmap(pixmap.scaled(
                340, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
            self.spec_label.setText("")

        except Exception as e:
            print(f"Ошибка спектрограммы: {e}")
            self.spec_label.setText(f"Не удалось построить\nспектрограмму")

    def _show_result(self, result):
        # Останавливаем прогресс бар
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)

        if result["status"] == "ok":
            best = result["best_match"]
            name = best["person"]["full_name"]
            similarity = best["similarity"] * 100
            confidence = best["confidence"]
            segments = result["segments"]
            analysis_time = result["analysis_time"]

            # Цвет в зависимости от уверенности
            if confidence == "высокая":
                color = "#10B981"
                badge_bg = "#ECFDF5"
                badge_border = "#10B981"
            elif confidence == "средняя":
                color = "#F59E0B"
                badge_bg = "#FFFBEB"
                badge_border = "#F59E0B"
            else:
                color = "#EF4444"
                badge_bg = "#FEF2F2"
                badge_border = "#EF4444"

            self.result_card.setStyleSheet(f"""
                QFrame {{
                    background: white;
                    border-radius: 10px;
                    border: 2px solid {color};
                }}
            """)

            self.result_name.setText(name)
            self.result_name.setStyleSheet(f"color: {color}; font-size: 18px; font-weight: bold; background: transparent; border: none;")
            self.result_meta.setText(
                f"Сходство: {similarity:.1f}%   ·   Уверенность: {confidence}\n"
                f"Сегментов проанализировано: {segments}"
            )
            self.status_label.setText("✓ Анализ завершён")
            self.status_label.setStyleSheet("color: #10B981; font-size: 12px; font-weight: bold; background: transparent;")
            self.time_label.setText(f"Время анализа: {analysis_time} сек")

            # Совпадения с прогресс-барами
            self._clear_matches()
            for i, (match_name, score) in enumerate(result["top_matches"]):
                self._add_match_row(i + 1, match_name, score, is_best=(i == 0))

        elif result["status"] == "not_found":
            self.result_card.setStyleSheet("""
                QFrame { background: white; border-radius: 10px; border: 2px solid #EF4444; }
            """)
            self.result_name.setText("Голос не найден")
            self.result_name.setStyleSheet("color: #EF4444; font-size: 18px; font-weight: bold; background: transparent; border: none;")
            self.result_meta.setText(f"Сегментов: {result.get('segments', '—')}   ·   Возможно, человек отсутствует в базе")
            self.status_label.setText("Голос не идентифицирован")
            self.status_label.setStyleSheet("color: #EF4444; font-size: 12px; font-weight: bold; background: transparent;")
            self.time_label.setText(f"Время анализа: {result.get('analysis_time', '—')} сек")

        else:
            self.result_name.setText("Ошибка анализа")
            self.result_name.setStyleSheet("color: #EF4444; font-size: 16px; font-weight: bold; background: transparent; border: none;")
            self.result_meta.setText(result.get("message", "Неизвестная ошибка"))
            self.status_label.setText("Ошибка")
            self.status_label.setStyleSheet("color: #EF4444; font-size: 12px; background: transparent;")

    def _clear_matches(self):
        while self.matches_inner.count():
            item = self.matches_inner.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _add_match_row(self, rank, name, score, is_best=False):
        """Добавляет строку совпадения с прогресс-баром"""
        row = QFrame()
        row.setCursor(Qt.PointingHandCursor)

        row.setStyleSheet(f"""
            QFrame {{
                background: {'#F0FDF4' if is_best else '#F8FAFC'};
                border-radius: 6px;
                border: 1px solid {'#BBF7D0' if is_best else '#E2E8F0'};
            }}
        """)
        row_layout = QVBoxLayout(row)
        row_layout.setContentsMargins(10, 8, 10, 8)
        row_layout.setSpacing(4)

        top_row = QHBoxLayout()

        rank_label = QLabel(f"#{rank}")
        rank_label.setFixedWidth(24)
        rank_label.setStyleSheet(f"color: {'#10B981' if is_best else '#94A3B8'}; font-size: 11px; font-weight: bold; background: transparent; border: none;")

        name_label = QLabel(name)
        name_label.setStyleSheet(f"color: {'#065F46' if is_best else '#1E293B'}; font-size: 13px; font-weight: {'bold' if is_best else 'normal'}; background: transparent; border: none;")

        pct = score * 100
        if pct >= 72:
            score_color = "#10B981"
        elif pct >= 65:
            score_color = "#F59E0B"
        else:
            score_color = "#EF4444"

        score_label = QLabel(f"{pct:.1f}%")
        score_label.setStyleSheet(f"color: {score_color}; font-size: 13px; font-weight: bold; background: transparent; border: none;")

        top_row.addWidget(rank_label)
        top_row.addWidget(name_label)
        top_row.addStretch()
        top_row.addWidget(score_label)
        row_layout.addLayout(top_row)

        bar = QProgressBar()
        bar.setFixedHeight(4)
        bar.setTextVisible(False)
        bar.setRange(0, 100)
        bar.setValue(int(pct))
        bar.setStyleSheet(f"""
            QProgressBar {{
                border: none; border-radius: 2px; background: #E2E8F0;
            }}
            QProgressBar::chunk {{
                background: {score_color}; border-radius: 2px;
            }}
        """)
        row_layout.addWidget(bar)

        row.mousePressEvent = lambda event, n=name: self._open_person(n)
        self.matches_inner.addWidget(row)

    def _open_person(self, name):
        if not self.db_manager:
            return

        people = self.db_manager.get_all_people()
        person = next((p for p in people if p['full_name'] == name), None)
        if person:
            dlg = PersonDetailsDialog(person, parent=self)
            dlg.exec()