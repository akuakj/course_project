from PySide6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit,
    QFrame, QListWidget, QListWidgetItem, QSpacerItem, QSizePolicy,
    QFileDialog
)
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtCore import Qt
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from datetime import datetime
import os


class PersonDetailsDialog(QDialog):
    def __init__(self, person_data, save_callback=None, parent=None):
        """
        person_data — dict с полями пользователя
        save_callback — функция сохранения в БД, если фото изменено
        """
        super().__init__(parent)
        self.person_data = person_data
        self.save_callback = save_callback
        self.player = None
        self.audio_output = None

        self.setWindowTitle("Детали записи")
        self.setFixedSize(650, 415)  # фиксированный размер окна

        self.init_ui()


    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # ============= [ РАМКА ДЛЯ ФОТО ] =============
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(150, 150)
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setStyleSheet("""
            QLabel {
                border: 2px solid #3498db;
                border-radius: 10px;
                background-color: #ecf0f1;
            }
        """)

        # Загрузить фото из БД, если есть
        photo_path = self.person_data.get("photo")
        if photo_path and os.path.exists(photo_path):
            self.set_photo(photo_path)

        # Клик по рамке для добавления фото
        self.photo_label.mousePressEvent = self.on_photo_clicked

        photo_layout = QVBoxLayout()
        photo_layout.addWidget(self.photo_label)
        photo_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        main_layout.addLayout(photo_layout)

        # ============= [ Блок информации справа ] =============
        info_frame = QFrame()
        info_layout = QVBoxLayout(info_frame)

        info_frame.setStyleSheet("""
            QLabel { font-size: 14px; color: #2c3e50; }
            QTextEdit { background-color: #fdfdfd; border: 1px solid #bdc3c7; border-radius: 5px; }
            QListWidget { border: 1px solid #bdc3c7; border-radius: 5px; }
            QPushButton { padding: 5px 10px; border-radius: 5px; background-color: #3498db; color: white; }
            QPushButton:hover { background-color: #2980b9; }
        """)

        # ФИО
        info_layout.addWidget(QLabel(f"<b>ФИО:</b> {self.person_data.get('full_name', '')}"))

        # Дата рождения
        info_layout.addWidget(QLabel(f"<b>Дата рождения:</b> {self.person_data.get('date_of_birth', '')}"))

        # Дата добавления
        created_at = self.person_data.get('created_at', '')
        try:
            created_fmt = datetime.fromisoformat(created_at).strftime("%Y-%m-%d %H:%M:%S")
        except:
            created_fmt = created_at

        info_layout.addWidget(QLabel(f"<b>Дата добавления:</b> {created_fmt}"))

        # Заметки
        info_layout.addWidget(QLabel("<b>Заметки:</b>"))
        notes = QTextEdit(self.person_data.get("notes", ""))
        notes.setReadOnly(True)
        notes.setFixedHeight(60)
        info_layout.addWidget(notes)

        # Векторные данные
        info_layout.addWidget(QLabel("<b>Векторные данные:</b>"))
        vector = QTextEdit(str(self.person_data.get("vector_data", [])))
        vector.setReadOnly(True)
        vector.setFixedHeight(100)
        info_layout.addWidget(vector)

        # --- Аудиофайлы ---
        info_layout.addWidget(QLabel("<b>Аудиофайлы:</b>"))
        audio_files = self.person_data.get("audio_files", [])
        self.audio_list = QListWidget()

        for f in audio_files:
            item = QListWidgetItem(os.path.basename(f))
            item.setData(Qt.UserRole, f)
            self.audio_list.addItem(item)

        row_height = self.audio_list.sizeHintForRow(0) if self.audio_list.count() else 20
        self.audio_list.setFixedHeight(min(len(audio_files), 5) * row_height + 2)

        info_layout.addWidget(self.audio_list)

        play_btn = QPushButton("▶ Прослушать выбранное аудио")
        play_btn.clicked.connect(self.play_audio)
        info_layout.addWidget(play_btn)

        info_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addWidget(info_frame)


    # -------------------------------------------------------
    # Фото — загрузка, отображение, выбор
    # -------------------------------------------------------
    def set_photo(self, path):
        """ Загружает и отображает изображение в рамке """
        pixmap = QPixmap(path)
        if pixmap.isNull():
            return

        # Масштабирование под рамку
        scaled = pixmap.scaled(
            self.photo_label.width(),
            self.photo_label.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.photo_label.setPixmap(scaled)


    def on_photo_clicked(self, event):
        """ Выбор фото по клику """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )
        if not file_path:
            return

        # Показать фото
        self.set_photo(file_path)

        # Обновить путь в данных пользователя
        self.person_data["photo"] = file_path

        # Сохранить в БД если дана функция сохранения
        if self.save_callback:
            self.save_callback(self.person_data)


    # -------------------------------------------------------
    # АУДИО
    # -------------------------------------------------------
    def play_audio(self):
        selected = self.audio_list.selectedItems()
        if not selected:
            return

        path = selected[0].data(Qt.UserRole)
        if not os.path.exists(path):
            return

        if self.player:
            self.player.stop()

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(path)
        self.audio_output.setVolume(50)
        self.player.play()
