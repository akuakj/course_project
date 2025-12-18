import os
import sounddevice as sd
import numpy as np
import soundfile as sf
from scipy.io.wavfile import write
from datetime import datetime
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PySide6.QtCore import QTimer, QThread, Signal
from gui.analysis import Ui_AnalysisDialog
import threading


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
        os.makedirs(self.output_dir, exist_ok=True)

    def setup_connections(self):
        """Подключение кнопок анализа"""
        self.main.btn_record_audio.clicked.connect(self.toggle_recording)
        self.main.btn_analysis_audio.clicked.connect(self.open_analysis_window)
        self.main.btn_load_audio.clicked.connect(self.load_audio)
        self.main.btn_start_audio.clicked.connect(self.start_audio)
        self.main.btn_pause_audio.clicked.connect(self.pause_audio)
        self.main.btn_close_audio.clicked.connect(self.close_audio)

    def toggle_recording(self):
        """Переключение между записью и остановкой"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """Начало записи аудио"""
        self.is_recording = True
        self.recorded_chunks = []
        self.main.btn_record_audio.setText("Остановить запись")

        # Запускаем поток записи
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.start()

    def _record_audio(self):
        """Запись аудио с микрофона"""
        with sd.InputStream(samplerate=self.record_sample_rate, channels=1, callback=self._callback):
            while self.is_recording:
                sd.sleep(100)

    def _callback(self, indata, frames, time, status):
        """Колбэк записи"""
        if status:
            print("Status:", status)
        self.recorded_chunks.append(indata.copy())

    def stop_recording(self):
        """Остановка записи и сохранение файла"""
        self.is_recording = False
        if self.recording_thread is not None:
            self.recording_thread.join()

        if not self.recorded_chunks:
            self.main.btn_record_audio.setText("Записать аудио")
            return

        # Объединяем данные
        audio_np = np.concatenate(self.recorded_chunks, axis=0)
        # Имя файла по дате и времени
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(self.output_dir, f"record_{timestamp}.wav")
        # Сохраняем
        write(filename, self.record_sample_rate, (audio_np * 32767).astype(np.int16))

        # Сброс кнопки
        self.main.btn_record_audio.setText("Записать аудио")

        # Автозагрузка
        self.current_audio_file = filename
        self.audio_data, self.sample_rate = sf.read(filename)
        if self.audio_data.ndim == 1:
            self.audio_data = self.audio_data.reshape(-1, 1)
        self.current_sample = 0
        self.main.label_file_name.setText(f"Файл: {os.path.basename(filename)}")
        self.main.btn_start_audio.setEnabled(True)
        self.main.btn_pause_audio.setEnabled(True)
        self.main.btn_close_audio.setEnabled(True)


    def load_audio(self):
        """Загрузка аудио файла"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.main, "Выберите аудио файл", "",
            "Аудио файлы (*.wav *.mp3 *.flac);;Все файлы (*)"
        )
        if file_path:
            try:
                self.current_audio_file = file_path
                self.audio_data, self.sample_rate = sf.read(file_path)
                if self.audio_data.ndim == 1:
                    self.audio_data = self.audio_data.reshape(-1, 1)
                self.current_sample = 0
                self.main.label_file_name.setText(f"Файл: {os.path.basename(file_path)}")
                self.main.progress_audio.setValue(0)
                self.main.btn_start_audio.setEnabled(True)
                self.main.btn_pause_audio.setEnabled(True)
                self.main.btn_close_audio.setEnabled(True)
            except Exception:
                self.main.label_file_name.setText("Ошибка: неподдерживаемый формат")

    def start_audio(self):
        if not self.current_audio_file or self.audio_data is None:
            return
        if not self.is_playing:
            # Если аудио дошло до конца, сбрасываем позицию
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
        if self.is_playing:
            progress_percent = min((self.current_sample / len(self.audio_data)) * 100, 100.0)
            self.main.progress_audio.setValue(int(progress_percent))
            if self.current_sample >= len(self.audio_data):
                self.stop_audio()
                self.main.progress_audio.setValue(100)

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
        self.main.label_file_name.setText('Файл не выбран')
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

from core.voice_analysis_service import VoiceAnalysisService

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

        # Показать прогресс
        self.textEdit_results.setText("⏳ Извлекаются голосовые признаки...")

        self.thread = AnalysisThread(audio_file)
        self.thread.finished_signal.connect(self.show_result)
        self.thread.start()

    def show_result(self, result):
        if result["status"] == "ok":
            text = f"🎤 Анализ завершён\n"
            text += f"👤 Найден голос: {result['best_match']['person']['full_name']}\n"
            text += f"📊 Сходство: {result['best_match']['similarity'] * 100:.1f}%\n"
            text += f"📈 Уверенность: {result['best_match']['confidence']}\n"
            text += f"🧩 Сегментов проанализировано: {result['segments']}\n"
            text += f"⏱ Время анализа: {result['analysis_time']} сек\n\n"
            text += f"🔍 Другие совпадения:\n"

            for i, (name, score) in enumerate(result["top_matches"], 1):
                confidence = "✅" if score >= 0.7 else "⚠️" if score >= 0.6 else "❌"
                text += f"{i}. {confidence} {name}: {score * 100:.1f}%\n"


            self.textEdit_results.setText(text)
            self.btn_save.setEnabled(True)

        elif result["status"] == "not_found":
            text = "❌ Голос не найден в базе.\n\n"
            text += f"Проанализировано сегментов: {result['segments']}\n"
            text += f"Время анализа: {result['analysis_time']} сек\n\n"
            text += "Возможные причины:\n"
            text += "1. Человек отсутствует в базе\n"
            text += "2. Аудио слишком короткое\n"
            text += "3. Сильный фоновый шум\n"
            text += "4. Низкое качество записи"
            self.textEdit_results.setText(text)

        else:
            self.textEdit_results.setText(f"❌ Ошибка анализа: {result.get('message', 'Неизвестная ошибка')}")