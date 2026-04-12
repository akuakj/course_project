import os
import numpy as np
import soundfile as sf
from PySide6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QFrame, QListWidget, QListWidgetItem,
    QFileDialog, QLineEdit, QDateEdit, QWidget, QProgressBar,
    QMessageBox
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QDate, QThread, Signal
from services.encoder_factory import create_encoder



#  Поток вычисления векторов
class VectorComputeThread(QThread):
    progress_signal = Signal(int, str)
    finished_signal = Signal(object)
 
    def __init__(self, audio_files: list[str]):
        super().__init__()
        self.audio_files = audio_files

    def run(self):
        try:

            encoder = create_encoder()
            embeddings = []
           
            total = len(self.audio_files)
 
            for i, path in enumerate(self.audio_files):
                # Прогресс: 0–90% на извлечение, 90–100% на усреднение
                progress = int((i / total) * 90)
                self.progress_signal.emit(
                    progress,
                    f"Обработка [{i+1}/{total}]: {os.path.basename(path)}"
                )
 
                try:
                    audio, sr = sf.read(path)
                    if audio.ndim > 1:
                        audio = audio.mean(axis=1)
 
                    emb = encoder.get_embedding(audio, sr)
                    if emb is not None:
                        embeddings.append(emb)
                    else:
                        print(f"[VectorComputeThread] Не удалось обработать: {path}")
 
                except Exception as e:
                    print(f"[VectorComputeThread] Ошибка файла {path}: {e}")
 
            if not embeddings:
                self.finished_signal.emit(None)
                return
 
            self.progress_signal.emit(95, "Усреднение векторов...")
 
            # Усредняем все эмбеддинги → один представительный вектор человека
            avg_vector = np.mean(embeddings, axis=0)
 
            self.progress_signal.emit(100, "Готово!")
            self.finished_signal.emit(avg_vector)
 
        except Exception as e:
            print(f"[VectorComputeThread] Критическая ошибка: {e}")
            self.finished_signal.emit(None)



#  Диалог добавления человека
class AddPersonDialog(QDialog):
    def __init__(self, db_manager, parent=None, on_saved=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.on_saved = on_saved
        self.audio_files = []
        self.photo_path = None
        self.computed_vector = None
        self.compute_thread = None

        self.setWindowTitle("Добавить человека")
        self.setFixedSize(680, 580)
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
        """)

        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── ШАПКА ──────────────────────────────
        header = QFrame()
        header.setFixedHeight(64)
        header.setStyleSheet("QFrame { background-color: #1a1f2e; border: none; }")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)

        title = QLabel("Добавить нового человека")
        title.setStyleSheet("color: white; font-size: 15px; font-weight: bold; background: transparent;")

        badge = QLabel("Новая запись")
        badge.setStyleSheet("""
            QLabel {
                background-color: rgba(52, 152, 219, 0.25);
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
        header_layout.addWidget(badge)
        main_layout.addWidget(header)

        #ТЕЛО
        body = QWidget()
        body.setStyleSheet("background-color: #F0F4F8;")
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(20, 20, 20, 10)
        body_layout.setSpacing(16)

        # ЛЕВАЯ КОЛОНКА — фото
        left_col = QVBoxLayout()
        left_col.setSpacing(12)

        photo_card = QFrame()
        photo_card.setFixedWidth(160)
        photo_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #E2E8F0;
            }
        """)
        photo_layout = QVBoxLayout(photo_card)
        photo_layout.setContentsMargins(12, 12, 12, 12)
        photo_layout.setSpacing(8)

        photo_lbl = self._section_label("ФОТО")
        self.photo_preview = QLabel()
        self.photo_preview.setFixedSize(136, 136)
        self.photo_preview.setAlignment(Qt.AlignCenter)
        self.photo_preview.setCursor(Qt.PointingHandCursor)
        self.photo_preview.setText("📷\nКликните для\nзагрузки фото")
        self.photo_preview.setStyleSheet("""
            QLabel {
                border: 2px dashed #CBD5E1;
                border-radius: 8px;
                background-color: #F8FAFC;
                color: #94A3B8;
                font-size: 11px;
            }
        """)
        self.photo_preview.mousePressEvent = self._pick_photo

        photo_layout.addWidget(photo_lbl)
        photo_layout.addWidget(self.photo_preview)
        left_col.addWidget(photo_card)
        left_col.addStretch()
        body_layout.addLayout(left_col)

        # ПРАВАЯ КОЛОНКА — поля
        right_col = QVBoxLayout()
        right_col.setSpacing(10)

        # Карточка основных полей
        fields_card = self._make_card()
        fields_layout = QVBoxLayout(fields_card)
        fields_layout.setContentsMargins(16, 14, 16, 14)
        fields_layout.setSpacing(10)

        field_style = """
            QLineEdit, QDateEdit {
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                padding: 7px 10px;
                font-size: 13px;
                color: #1E293B;
                background: white;
            }
            QLineEdit:focus, QDateEdit:focus { border-color: #3B82F6; }
        """

        fields_layout.addWidget(self._section_label("ФИО *"))
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Введите полное имя...")
        self.input_name.setStyleSheet(field_style)
        fields_layout.addWidget(self.input_name)

        fields_layout.addWidget(self._section_label("ДАТА РОЖДЕНИЯ"))
        self.input_dob = QDateEdit()
        self.input_dob.setCalendarPopup(True)
        self.input_dob.setDisplayFormat("dd.MM.yyyy")
        self.input_dob.setDate(QDate.currentDate())
        self.input_dob.setStyleSheet(field_style)
        fields_layout.addWidget(self.input_dob)

        fields_layout.addWidget(self._section_label("ЗАМЕТКИ"))
        self.input_notes = QTextEdit()
        self.input_notes.setFixedHeight(60)
        self.input_notes.setPlaceholderText("Необязательно...")
        self.input_notes.setStyleSheet("""
            QTextEdit {
                border: 1px solid #E2E8F0; border-radius: 6px;
                padding: 6px 8px; font-size: 13px;
                color: #1E293B; background: white;
            }
            QTextEdit:focus { border-color: #3B82F6; }
        """)
        fields_layout.addWidget(self.input_notes)
        right_col.addWidget(fields_card)

        # Карточка аудиофайлов
        audio_card = self._make_card()
        audio_layout = QVBoxLayout(audio_card)
        audio_layout.setContentsMargins(16, 12, 16, 12)
        audio_layout.setSpacing(8)

        audio_header = QHBoxLayout()
        audio_header.addWidget(self._section_label("АУДИОФАЙЛЫ *"))
        audio_header.addStretch()

        self.label_audio_count = QLabel("0 файлов")
        self.label_audio_count.setStyleSheet("""
            QLabel {
                background-color: #F1F5F9;
                color: #64748B;
                border-radius: 8px;
                font-size: 11px;
                font-weight: bold;
                padding: 2px 8px;
                border: none;
            }
        """)
        audio_header.addWidget(self.label_audio_count)
        audio_layout.addLayout(audio_header)

        self.audio_list = QListWidget()
        self.audio_list.setFixedHeight(80)
        self.audio_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #E2E8F0; border-radius: 6px;
                background-color: #F8FAFC; font-size: 12px; color: #475569; outline: none;
            }
            QListWidget::item { padding: 4px 6px; border-radius: 4px; }
            QListWidget::item:selected { background-color: #EFF6FF; color: #2563EB; }
            QListWidget::item:hover { background-color: #F1F5F9; }
        """)
        audio_layout.addWidget(self.audio_list)

        audio_btns = QHBoxLayout()
        add_audio_btn = QPushButton("  ADD FILE  ")
        add_audio_btn.setFixedHeight(30)
        add_audio_btn.setCursor(Qt.PointingHandCursor)
        add_audio_btn.clicked.connect(self._add_audio_files)
        add_audio_btn.setStyleSheet("""
            QPushButton {
                background-color: #EFF6FF; color: #3B82F6;
                border: 1px solid #BFDBFE; border-radius: 6px;
                font-size: 12px; font-weight: bold;
            }
            QPushButton:hover { background-color: #DBEAFE; }
        """)

        remove_audio_btn = QPushButton("  DELETE  ")
        remove_audio_btn.setFixedHeight(30)
        remove_audio_btn.setCursor(Qt.PointingHandCursor)
        remove_audio_btn.clicked.connect(self._remove_audio_file)
        remove_audio_btn.setStyleSheet("""
            QPushButton {
                background-color: #FEF2F2; color: #EF4444;
                border: 1px solid #FECACA; border-radius: 6px;
                font-size: 12px; font-weight: bold;
            }
            QPushButton:hover { background-color: #FEE2E2; }
        """)
        audio_btns.addWidget(add_audio_btn)
        audio_btns.addWidget(remove_audio_btn)
        audio_btns.addStretch()
        audio_layout.addLayout(audio_btns)
        right_col.addWidget(audio_card)

        # Прогресс бар вычисления вектора
        self.progress_card = self._make_card()
        self.progress_card.hide()
        progress_layout = QVBoxLayout(self.progress_card)
        progress_layout.setContentsMargins(16, 12, 16, 12)
        progress_layout.setSpacing(6)
        self.progress_label = QLabel("Вычисление вектора...")
        self.progress_label.setStyleSheet("color: #475569; font-size: 12px; background: transparent; border: none;")
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none; border-radius: 4px;
                background-color: #E2E8F0;
            }
            QProgressBar::chunk {
                background-color: #3B82F6; border-radius: 4px;
            }
        """)
        self.progress_bar.setTextVisible(False)
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)
        right_col.addWidget(self.progress_card)

        right_col.addStretch()
        body_layout.addLayout(right_col)
        main_layout.addWidget(body)

        # ФУТЕР
        footer = QFrame()
        footer.setFixedHeight(58)
        footer.setStyleSheet("QFrame { background-color: white; border-top: 1px solid #E2E8F0; border: none; }")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(20, 0, 20, 0)

        hint = QLabel("* обязательные поля")
        hint.setStyleSheet("color: #94A3B8; font-size: 11px;")

        self.save_btn = QPushButton("💾  Сохранить")
        self.save_btn.setFixedSize(130, 36)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self._save)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                border: none; border-radius: 6px;
                font-size: 12px; font-weight: bold;
            }
            QPushButton:hover:enabled { background-color: #219a52; }
            QPushButton:disabled { background-color: #CBD5E1; color: #94A3B8; }
        """)

        cancel_btn = QPushButton("Отмена")
        cancel_btn.setFixedSize(90, 36)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.clicked.connect(self.close)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a1f2e; color: #94A3B8;
                border: none; border-radius: 6px;
                font-size: 12px; font-weight: bold;
            }
            QPushButton:hover { background-color: #2d3447; color: white; }
        """)

        footer_layout.addWidget(hint)
        footer_layout.addStretch()
        footer_layout.addWidget(self.save_btn)
        footer_layout.addSpacing(8)
        footer_layout.addWidget(cancel_btn)
        main_layout.addWidget(footer)

    # Вспомогательные методы
    def _make_card(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #E2E8F0;
            }
        """)
        return card

    def _section_label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("""
            QLabel {
                color: #94A3B8; font-size: 10px; font-weight: bold;
                letter-spacing: 1px; background: transparent; border: none;
            }
        """)
        return lbl

    def _pick_photo(self, event):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите фото", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if path:
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(136, 136, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.photo_preview.setPixmap(scaled)
                self.photo_preview.setStyleSheet("""
                    QLabel { border: 2px solid #10B981; border-radius: 8px; background-color: #F0FDF4; }
                """)
                self.photo_path = path

    def _add_audio_files(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Выберите аудиофайлы", "",
            "Аудио файлы (*.wav *.mp3 *.flac)"
        )
        for path in paths:
            if path not in self.audio_files:
                self.audio_files.append(path)
                item = QListWidgetItem(f"🎵  {os.path.basename(path)}")
                item.setData(Qt.UserRole, path)
                self.audio_list.addItem(item)

        self.label_audio_count.setText(f"{len(self.audio_files)} файлов")

    def _remove_audio_file(self):
        selected = self.audio_list.selectedItems()
        if not selected:
            return
        for item in selected:
            path = item.data(Qt.UserRole)
            if path in self.audio_files:
                self.audio_files.remove(path)
            self.audio_list.takeItem(self.audio_list.row(item))
        self.label_audio_count.setText(f"{len(self.audio_files)} файлов")

    # Сохранение
    def _save(self):
        name = self.input_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите ФИО")
            return

        if len(self.audio_files) < 2:
            QMessageBox.warning(self, "Ошибка",
                "Добавьте минимум 2 аудиофайла для надёжной идентификации")
            return

        # Запускаем вычисление вектора в отдельном потоке
        self.save_btn.setEnabled(False)
        self.progress_card.show()
        self.progress_bar.setValue(0)

        self.compute_thread = VectorComputeThread(self.audio_files)
        self.compute_thread.progress_signal.connect(self._on_progress)
        self.compute_thread.finished_signal.connect(self._on_vector_ready)
        self.compute_thread.start()

    def _on_progress(self, value, message):
        self.progress_bar.setValue(value)
        self.progress_label.setText(message)

    def _on_vector_ready(self, vector):
        if vector is None:
            QMessageBox.critical(self, "Ошибка",
                "Не удалось вычислить голосовой вектор.\nПроверьте аудиофайлы.")
            self.save_btn.setEnabled(True)
            self.progress_card.hide()
            return

        try:
            record_id = self.db_manager.add_voice_person(
                full_name=self.input_name.text().strip(),
                audio_files=self.audio_files,
                vector_data=vector,
                notes=self.input_notes.toPlainText().strip(),
                date_of_birth=self.input_dob.date().toString("dd.MM.yyyy"),
                photo=self.photo_path
            )

            if record_id:
                QMessageBox.information(self, "Успех",
                    f"Человек успешно добавлен в базу данных!")
                if self.on_saved:
                    self.on_saved()
                self.close()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось сохранить запись")
                self.save_btn.setEnabled(True)
                self.progress_card.hide()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения: {e}")
            self.save_btn.setEnabled(True)
            self.progress_card.hide()
