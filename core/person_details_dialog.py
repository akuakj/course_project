from PySide6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit,
    QFrame, QListWidget, QListWidgetItem, QSpacerItem, QSizePolicy,
    QFileDialog, QLineEdit, QDateEdit, QStackedWidget, QScrollArea, QWidget
)
from PySide6.QtGui import QPixmap, Qt, QIcon
from PySide6.QtCore import Qt, QDate
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from datetime import datetime
import os


class PersonDetailsDialog(QDialog):
    def __init__(self, person_data, save_callback=None, parent=None):
        super().__init__(parent)
        self.person_data = person_data
        self.save_callback = save_callback
        self.player = None
        self.audio_output = None
        self.is_edit_mode = False
        self.original_photo_path = person_data.get("photo")

        self.setWindowTitle("Детали записи")
        self.setFixedSize(700, 544)  # Увеличим для вектора

        self.init_ui()
        self.init_edit_controls()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # ============= [ ШАПКА С КНОПКОЙ РЕДАКТИРОВАНИЯ ] =============
        header_layout = QHBoxLayout()

        title_label = QLabel("Информация о человеке")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")

        self.edit_btn = QPushButton()
        self.edit_btn.setIcon(QIcon("✏️"))
        self.edit_btn.setText(" Редактировать")
        self.edit_btn.setFixedSize(120, 30)
        self.edit_btn.clicked.connect(self.toggle_edit_mode)
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.edit_btn)

        main_layout.addLayout(header_layout)

        # ============= [ ОСНОВНОЕ СОДЕРЖИМОЕ С ПРОКРУТКОЙ ] =============
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QHBoxLayout(scroll_widget)

        # ЛЕВАЯ КОЛОНКА: Фото
        left_column = QVBoxLayout()

        self.photo_label = QLabel()
        self.photo_label.setFixedSize(150, 150)
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #3498db;
                border-radius: 10px;
                background-color: #f8f9fa;
            }
        """)

        photo_path = self.person_data.get("photo")
        if photo_path and os.path.exists(photo_path):
            self.set_photo(photo_path)
        else:
            self.photo_label.setText("📷\nКликните для\nзагрузки фото")
            self.photo_label.setStyleSheet("""
                QLabel {
                    border: 2px dashed #95a5a6;
                    border-radius: 10px;
                    background-color: #f8f9fa;
                    color: #7f8c8d;
                    font-size: 12px;
                }
            """)

        self.photo_label.mousePressEvent = self.on_photo_clicked

        left_column.addWidget(self.photo_label)
        left_column.addStretch()

        scroll_layout.addLayout(left_column)

        # ПРАВАЯ КОЛОНКА: Информация с stacked widget
        right_column = QVBoxLayout()

        self.info_stack = QStackedWidget()

        self.view_widget = self.create_view_widget()
        self.edit_widget = self.create_edit_widget()

        self.info_stack.addWidget(self.view_widget)
        self.info_stack.addWidget(self.edit_widget)

        right_column.addWidget(self.info_stack)
        scroll_layout.addLayout(right_column)

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        # ============= [ КНОПКИ ВНИЗУ ] =============
        button_layout = QHBoxLayout()

        self.save_btn = QPushButton("💾 Сохранить изменения")
        self.save_btn.clicked.connect(self.save_changes)
        self.save_btn.setFixedSize(180, 35)
        self.save_btn.setEnabled(False)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)

        self.cancel_btn = QPushButton("❌ Отменить")
        self.cancel_btn.clicked.connect(self.cancel_edit)
        self.cancel_btn.setFixedSize(120, 35)
        self.cancel_btn.setEnabled(False)

        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.close)
        close_btn.setFixedSize(100, 35)

        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(close_btn)

        main_layout.addLayout(button_layout)

    def create_view_widget(self):
        """Создает виджет для режима просмотра"""
        widget = QFrame()
        layout = QVBoxLayout(widget)

        # ФИО
        self.view_full_name = QLabel(f"<b>ФИО:</b> {self.person_data.get('full_name', '')}")
        layout.addWidget(self.view_full_name)

        # Дата рождения
        dob = self.person_data.get('date_of_birth', '')
        self.view_dob = QLabel(f"<b>Дата рождения:</b> {dob if dob else 'Не указана'}")
        layout.addWidget(self.view_dob)

        # Дата добавления
        created_at = self.person_data.get('created_at', '')
        try:
            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            created_fmt = dt.strftime("%d.%m.%Y %H:%M")
        except:
            created_fmt = created_at[:19] if len(created_at) > 19 else created_at
        layout.addWidget(QLabel(f"<b>Дата добавления:</b> {created_fmt}"))

        # Заметки
        layout.addWidget(QLabel("<b>Заметки:</b>"))
        self.view_notes = QTextEdit(self.person_data.get("notes", ""))
        self.view_notes.setReadOnly(True)
        self.view_notes.setFixedHeight(60)
        layout.addWidget(self.view_notes)

        # ВЕКТОРНЫЕ ДАННЫЕ (компактно с кнопкой)
        layout.addWidget(QLabel("<b>Векторные данные:</b>"))

        vector_data = self.person_data.get("vector_data", [])
        if vector_data:
            vector_length = len(vector_data)
            if vector_length > 10:
                first = ', '.join(f"{x:.4f}" for x in vector_data[:3])
                last = ', '.join(f"{x:.4f}" for x in vector_data[-3:])
                vector_text = f"Длина: {vector_length} элементов\n[{first}, ..., {last}]"
            else:
                vector_text = f"[{', '.join(f'{x:.4f}' for x in vector_data)}]"
        else:
            vector_text = "[]"

        vector_display = QTextEdit(vector_text)
        vector_display.setReadOnly(True)
        vector_display.setFixedHeight(60)
        vector_display.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        layout.addWidget(vector_display)

        # Кнопка для полного просмотра вектора
        self.view_vector_btn = QPushButton("📊 Показать полный вектор")
        self.view_vector_btn.clicked.connect(self.show_full_vector)
        self.view_vector_btn.setFixedHeight(25)
        self.view_vector_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        layout.addWidget(self.view_vector_btn)

        # Аудиофайлы
        layout.addWidget(QLabel("<b>Аудиофайлы:</b>"))

        audio_files = self.person_data.get("audio_files", [])
        self.audio_list = QListWidget()

        for f in audio_files:
            item = QListWidgetItem(os.path.basename(f))
            item.setData(Qt.UserRole, f)
            self.audio_list.addItem(item)

        self.audio_list.setFixedHeight(80)
        self.audio_list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        layout.addWidget(self.audio_list)

        play_btn = QPushButton("▶️ Прослушать выбранное аудио")
        play_btn.clicked.connect(self.play_audio)
        play_btn.setFixedHeight(25)

        layout.addWidget(play_btn)
        play_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #229954;
            }
        """)

        layout.addStretch()
        return widget

    def create_edit_widget(self):
        """Создает виджет для режима редактирования"""
        widget = QFrame()
        layout = QVBoxLayout(widget)

        # ФИО (редактирование)
        layout.addWidget(QLabel("<b>ФИО:</b>"))
        self.edit_full_name = QLineEdit(self.person_data.get('full_name', ''))
        self.edit_full_name.setPlaceholderText("Введите ФИО")
        layout.addWidget(self.edit_full_name)

        # Дата рождения (редактирование)
        layout.addWidget(QLabel("<b>Дата рождения:</b>"))
        self.edit_dob = QDateEdit()
        self.edit_dob.setCalendarPopup(True)
        self.edit_dob.setDisplayFormat("dd.MM.yyyy")

        dob_str = self.person_data.get('date_of_birth', '')
        if dob_str:
            try:
                dob_date = QDate.fromString(dob_str, "dd.MM.yyyy")
                if dob_date.isValid():
                    self.edit_dob.setDate(dob_date)
            except:
                pass

        layout.addWidget(self.edit_dob)

        # Дата добавления (только чтение)
        created_at = self.person_data.get('created_at', '')
        try:
            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            created_fmt = dt.strftime("%d.%m.%Y %H:%M")
        except:
            created_fmt = created_at[:19] if len(created_at) > 19 else created_at
        layout.addWidget(QLabel(f"<b>Дата добавления:</b> {created_fmt}"))

        # Заметки (редактирование)
        layout.addWidget(QLabel("<b>Заметки:</b>"))
        self.edit_notes = QTextEdit(self.person_data.get("notes", ""))
        self.edit_notes.setFixedHeight(70)
        layout.addWidget(self.edit_notes)

        # Векторные данные (только просмотр в режиме редактирования)
        layout.addWidget(QLabel("<b>Векторные данные (только чтение):</b>"))

        vector_data = self.person_data.get("vector_data", [])
        if vector_data:
            vector_length = len(vector_data)
            vector_text = f"Длина вектора: {vector_length} элементов\nИзменить нельзя"
        else:
            vector_text = "Вектор отсутствует"

        vector_info = QLabel(vector_text)
        vector_info.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addWidget(vector_info)

        layout.addStretch()
        return widget

    def init_edit_controls(self):
        """Инициализация элементов управления редактированием"""
        self.info_stack.setCurrentIndex(0)

    def toggle_edit_mode(self):
        """Переключение между режимами просмотра и редактирования"""
        self.is_edit_mode = not self.is_edit_mode

        if self.is_edit_mode:
            self.info_stack.setCurrentIndex(1)
            self.edit_btn.setText(" 👁️ Просмотр")
            self.edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f39c12;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #d68910;
                }
            """)
            self.save_btn.setEnabled(True)
            self.cancel_btn.setEnabled(True)
            self.view_vector_btn.setEnabled(False)  # Отключаем в режиме редактирования
        else:
            self.info_stack.setCurrentIndex(0)
            self.edit_btn.setText(" ✏️ Редактировать")
            self.edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            self.save_btn.setEnabled(False)
            self.cancel_btn.setEnabled(False)
            self.view_vector_btn.setEnabled(True)  # Включаем обратно

    def save_changes(self):
        """Сохранение изменений"""
        try:
            from PySide6.QtWidgets import QMessageBox

            updated_data = {
                'full_name': self.edit_full_name.text().strip(),
                'date_of_birth': self.edit_dob.date().toString("dd.MM.yyyy"),
                'notes': self.edit_notes.toPlainText().strip(),
                'photo': self.person_data.get('photo')
            }

            if not updated_data['full_name']:
                QMessageBox.warning(self, "Ошибка", "ФИО не может быть пустым")
                return

            # Обновляем локальные данные
            self.person_data.update(updated_data)

            # Обновляем вид просмотра
            self.view_full_name.setText(f"<b>ФИО:</b> {updated_data['full_name']}")
            self.view_dob.setText(f"<b>Дата рождения:</b> {updated_data['date_of_birth']}")
            self.view_notes.setPlainText(updated_data['notes'])

            # Сохраняем в БД
            if self.save_callback:
                self.save_callback(self.person_data)

            # Переключаемся обратно
            self.toggle_edit_mode()

            QMessageBox.information(self, "Успех", "Данные успешно сохранены!")

        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить данные: {e}")

    def cancel_edit(self):
        """Отмена редактирования"""
        self.edit_full_name.setText(self.person_data.get('full_name', ''))

        dob_str = self.person_data.get('date_of_birth', '')
        if dob_str:
            try:
                dob_date = QDate.fromString(dob_str, "dd.MM.yyyy")
                if dob_date.isValid():
                    self.edit_dob.setDate(dob_date)
            except:
                pass

        self.edit_notes.setPlainText(self.person_data.get('notes', ''))

        if self.original_photo_path and os.path.exists(self.original_photo_path):
            self.set_photo(self.original_photo_path)
            self.person_data['photo'] = self.original_photo_path

        self.toggle_edit_mode()

    def set_photo(self, path):
        """Загружает и отображает изображение"""
        try:
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    self.photo_label.width(),
                    self.photo_label.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.photo_label.setPixmap(scaled)
                self.person_data['photo'] = path
                self.photo_label.setStyleSheet("""
                    QLabel {
                        border: 2px solid #27ae60;
                        border-radius: 10px;
                    }
                """)
        except Exception as e:
            print(f"Ошибка загрузки фото: {e}")

    def on_photo_clicked(self, event):
        """Выбор фото по клику"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.set_photo(file_path)

    def play_audio(self):
        """Воспроизведение выбранного аудио"""
        selected = self.audio_list.selectedItems()
        if not selected:
            return

        path = selected[0].data(Qt.UserRole)
        if not os.path.exists(path):
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Ошибка", f"Файл не найден:\n{path}")
            return

        if self.player:
            self.player.stop()

        try:
            self.player = QMediaPlayer()
            self.audio_output = QAudioOutput()
            self.player.setAudioOutput(self.audio_output)
            self.player.setSource(path)
            self.audio_output.setVolume(50)
            self.player.play()
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Ошибка", f"Не удалось воспроизвести аудио: {e}")

    def show_full_vector(self):
        """Показать полный вектор в отдельном окне"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout

        dlg = QDialog(self)
        dlg.setWindowTitle(f"Векторные данные - {self.person_data.get('full_name', '')}")
        dlg.setFixedSize(600, 500)

        layout = QVBoxLayout(dlg)

        vector_data = self.person_data.get("vector_data", [])
        info_label = QLabel(f"Длина вектора: {len(vector_data)} элементов")
        layout.addWidget(info_label)

        text_edit = QTextEdit()
        text_edit.setPlainText(str(vector_data))
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("""
            QTextEdit {
                font-family: 'Courier New';
                font-size: 10pt;
            }
        """)
        layout.addWidget(text_edit)

        btn_layout = QHBoxLayout()

        copy_btn = QPushButton("📋 Копировать")
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(str(vector_data)))

        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(dlg.close)

        btn_layout.addWidget(copy_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        dlg.exec()

    def copy_to_clipboard(self, text):
        """Копировать текст в буфер обмена"""
        from PySide6.QtGui import QGuiApplication
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(text)