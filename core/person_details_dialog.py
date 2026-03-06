from PySide6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit,
    QFrame, QListWidget, QListWidgetItem, QSpacerItem, QSizePolicy,
    QFileDialog, QLineEdit, QDateEdit, QStackedWidget, QScrollArea, QWidget,
    QGraphicsDropShadowEffect
)
from PySide6.QtGui import QPixmap, QIcon, QColor, QFont
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
        self.setFixedSize(720, 560)
        self.setStyleSheet("""
            QDialog {
                background-color: #F0F4F8;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 6px;
                margin: 4px 2px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: #CBD5E1;
                border-radius: 3px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94A3B8;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
            QScrollBar:horizontal {
                height: 6px;
                background: transparent;
                margin: 2px 4px;
                border-radius: 3px;
            }
            QScrollBar::handle:horizontal {
                background: #CBD5E1;
                border-radius: 3px;
                min-width: 30px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #94A3B8;
            }
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)

        self.init_ui()
        self.init_edit_controls()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── ШАПКА ──────────────────────────────────────────
        header = QFrame()
        header.setFixedHeight(64)
        header.setStyleSheet("""
            QFrame {
                background-color: #1a1f2e;
                border: none;
            }
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)

        title_label = QLabel("Информация о человеке")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 15px;
                font-weight: bold;
                background: transparent;
            }
        """)

        self.edit_btn = QPushButton("✏  Редактировать")
        self.edit_btn.setFixedSize(145, 34)
        self.edit_btn.setCursor(Qt.PointingHandCursor)
        self.edit_btn.clicked.connect(self.toggle_edit_mode)
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                padding: 0 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.edit_btn)
        main_layout.addWidget(header)

        # ── ТЕЛО ───────────────────────────────────────────
        body = QWidget()
        body.setStyleSheet("background-color: #F0F4F8;")
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(20, 20, 20, 10)
        body_layout.setSpacing(16)

        # ЛЕВАЯ КОЛОНКА — фото + аудио
        left_col = QVBoxLayout()
        left_col.setSpacing(12)

        # Карточка фото
        photo_card = QFrame()
        photo_card.setFixedWidth(170)
        photo_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #E2E8F0;
            }
        """)
        photo_card_layout = QVBoxLayout(photo_card)
        photo_card_layout.setContentsMargins(12, 12, 12, 12)
        photo_card_layout.setSpacing(8)

        card_label = QLabel("ФОТО")
        card_label.setStyleSheet("""
            QLabel {
                color: #94A3B8;
                font-size: 10px;
                font-weight: bold;
                letter-spacing: 1px;
                background: transparent;
                border: none;
            }
        """)

        self.photo_label = QLabel()
        self.photo_label.setFixedSize(146, 146)
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setCursor(Qt.PointingHandCursor)
        self.photo_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #CBD5E1;
                border-radius: 8px;
                background-color: #F8FAFC;
                color: #94A3B8;
                font-size: 11px;
            }
        """)

        photo_path = self.person_data.get("photo")
        if photo_path and os.path.exists(photo_path):
            self.set_photo(photo_path)
        else:
            self.photo_label.setText("📷\nКликните для\nзагрузки фото")

        self.photo_label.mousePressEvent = self.on_photo_clicked

        photo_card_layout.addWidget(card_label)
        photo_card_layout.addWidget(self.photo_label)
        left_col.addWidget(photo_card)

        # Карточка аудиофайлов
        audio_card = QFrame()
        audio_card.setFixedWidth(170)
        audio_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #E2E8F0;
            }
        """)
        audio_card_layout = QVBoxLayout(audio_card)
        audio_card_layout.setContentsMargins(12, 12, 12, 12)
        audio_card_layout.setSpacing(8)

        audio_label = QLabel("АУДИОФАЙЛЫ")
        audio_label.setStyleSheet("""
            QLabel {
                color: #94A3B8;
                font-size: 10px;
                font-weight: bold;
                letter-spacing: 1px;
                background: transparent;
                border: none;
            }
        """)

        self.audio_list = QListWidget()
        self.audio_list.setMaximumHeight(120)
        self.audio_list.setMinimumHeight(0)
        self.audio_list.setSizeAdjustPolicy(QListWidget.SizeAdjustPolicy.AdjustToContents)
        self.audio_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                background-color: #F8FAFC;
                font-size: 12px;
                color: #475569;
                outline: none;
            }
            QListWidget::item {
                padding: 4px 6px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #EFF6FF;
                color: #2563EB;
            }
            QListWidget::item:hover {
                background-color: #F1F5F9;
            }
        """)

        audio_files = self.person_data.get("audio_files", [])
        for af in audio_files:
            item = QListWidgetItem(os.path.basename(af))
            item.setData(Qt.UserRole, af)
            self.audio_list.addItem(item)

        play_btn = QPushButton("▶  Прослушать")
        play_btn.setFixedHeight(32)
        play_btn.setCursor(Qt.PointingHandCursor)
        play_btn.clicked.connect(self.play_audio)
        play_btn.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)

        audio_card_layout.addWidget(audio_label)
        audio_card_layout.addWidget(self.audio_list)
        audio_card_layout.addWidget(play_btn)
        left_col.addWidget(audio_card)
        left_col.addStretch()

        body_layout.addLayout(left_col)

        # ПРАВАЯ КОЛОНКА — инфо
        right_col = QVBoxLayout()
        right_col.setSpacing(0)

        self.info_stack = QStackedWidget()
        self.view_widget = self.create_view_widget()
        self.edit_widget = self.create_edit_widget()
        self.info_stack.addWidget(self.view_widget)
        self.info_stack.addWidget(self.edit_widget)

        right_col.addWidget(self.info_stack)
        body_layout.addLayout(right_col)

        main_layout.addWidget(body)

        # ── НИЖНЯЯ ПАНЕЛЬ ──────────────────────────────────
        footer = QFrame()
        footer.setFixedHeight(58)
        footer.setStyleSheet("""
            QFrame {
                background-color: white;
                border-top: 1px solid #E2E8F0;
                border: none;
            }
        """)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(20, 0, 20, 0)

        self.save_btn = QPushButton("💾  Сохранить")
        self.save_btn.setFixedSize(130, 36)
        self.save_btn.setEnabled(False)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_changes)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #219a52;
            }
            QPushButton:disabled {
                background-color: #CBD5E1;
                color: #94A3B8;
            }
        """)

        self.cancel_btn = QPushButton("✕  Отменить")
        self.cancel_btn.setFixedSize(110, 36)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        self.cancel_btn.clicked.connect(self.cancel_edit)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #F1F5F9;
                color: #64748B;
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #E2E8F0;
                color: #E74C3C;
                border-color: #E74C3C;
            }
            QPushButton:disabled {
                color: #CBD5E1;
                border-color: #F1F5F9;
            }
        """)

        close_btn = QPushButton("Закрыть")
        close_btn.setFixedSize(90, 36)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a1f2e;
                color: #94A3B8;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2d3447;
                color: white;
            }
        """)

        footer_layout.addStretch()
        footer_layout.addWidget(self.save_btn)
        footer_layout.addSpacing(8)
        footer_layout.addWidget(self.cancel_btn)
        footer_layout.addSpacing(8)
        footer_layout.addWidget(close_btn)

        main_layout.addWidget(footer)

    def _make_info_card(self):
        """Создаёт белую карточку для контента"""
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
                color: #94A3B8;
                font-size: 10px;
                font-weight: bold;
                letter-spacing: 1px;
                background: transparent;
                border: none;
            }
        """)
        return lbl

    def _value_label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("""
            QLabel {
                color: #1E293B;
                font-size: 13px;
                background: transparent;
                border: none;
            }
        """)
        return lbl

    def create_view_widget(self):
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Карточка с основной инфо
        info_card = self._make_info_card()
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(16, 14, 16, 14)
        info_layout.setSpacing(10)

        # ФИО
        fio_row = QVBoxLayout()
        fio_row.setSpacing(2)
        fio_row.addWidget(self._section_label("ФИО"))
        self.view_full_name = self._value_label(self.person_data.get('full_name', ''))
        self.view_full_name.setStyleSheet("""
            QLabel {
                color: #1E293B;
                font-size: 15px;
                font-weight: bold;
                background: transparent;
                border: none;
            }
        """)
        fio_row.addWidget(self.view_full_name)
        info_layout.addLayout(fio_row)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("border: none; border-top: 1px solid #F1F5F9;")
        info_layout.addWidget(sep)

        # Дата рождения + дата добавления в ряд
        dates_row = QHBoxLayout()
        dates_row.setSpacing(20)

        dob_col = QVBoxLayout()
        dob_col.setSpacing(2)
        dob_col.addWidget(self._section_label("ДАТА РОЖДЕНИЯ"))
        dob = self.person_data.get('date_of_birth', '')
        self.view_dob = self._value_label(dob if dob else "Не указана")
        dob_col.addWidget(self.view_dob)
        dates_row.addLayout(dob_col)

        added_col = QVBoxLayout()
        added_col.setSpacing(2)
        added_col.addWidget(self._section_label("ДАТА ДОБАВЛЕНИЯ"))
        created_at = self.person_data.get('created_at', '')
        try:
            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            created_fmt = dt.strftime("%d.%m.%Y %H:%M")
        except Exception:
            created_fmt = created_at[:19] if len(created_at) > 19 else created_at
        added_col.addWidget(self._value_label(created_fmt))
        dates_row.addLayout(added_col)
        dates_row.addStretch()
        info_layout.addLayout(dates_row)

        layout.addWidget(info_card)

        # Карточка заметок
        notes_card = self._make_info_card()
        notes_layout = QVBoxLayout(notes_card)
        notes_layout.setContentsMargins(16, 12, 16, 12)
        notes_layout.setSpacing(6)
        notes_layout.addWidget(self._section_label("ЗАМЕТКИ"))

        self.view_notes = QTextEdit(self.person_data.get("notes", ""))
        self.view_notes.setReadOnly(True)
        self.view_notes.setFixedHeight(58)
        self.view_notes.setStyleSheet("""
            QTextEdit {
                border: none;
                background: transparent;
                font-size: 13px;
                color: #475569;
            }
        """)
        notes_layout.addWidget(self.view_notes)
        layout.addWidget(notes_card)

        # Карточка вектора
        vector_card = self._make_info_card()
        vector_layout = QVBoxLayout(vector_card)
        vector_layout.setContentsMargins(16, 12, 16, 12)
        vector_layout.setSpacing(6)

        vec_header = QHBoxLayout()
        vec_header.addWidget(self._section_label("ВЕКТОРНЫЕ ДАННЫЕ"))
        vec_header.addStretch()

        self.view_vector_btn = QPushButton("📊 Полный вектор")
        self.view_vector_btn.setFixedSize(130, 26)
        self.view_vector_btn.setCursor(Qt.PointingHandCursor)
        self.view_vector_btn.clicked.connect(self.show_full_vector)
        self.view_vector_btn.setStyleSheet("""
            QPushButton {
                background-color: #EFF6FF;
                color: #3B82F6;
                border: 1px solid #BFDBFE;
                border-radius: 5px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #DBEAFE;
            }
        """)
        vec_header.addWidget(self.view_vector_btn)
        vector_layout.addLayout(vec_header)

        vector_data = self.person_data.get("vector_data", [])
        if vector_data:
            n = len(vector_data)
            first = ', '.join(f"{x:.4f}" for x in vector_data[:3])
            last = ', '.join(f"{x:.4f}" for x in vector_data[-3:])
            vec_text = f"Длина: {n} элементов  [{first}, ..., {last}]"
        else:
            vec_text = "Вектор отсутствует"

        vec_display = QLabel(vec_text)
        vec_display.setStyleSheet("""
            QLabel {
                color: #64748B;
                font-size: 11px;
                font-family: 'Courier New';
                background: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 5px;
                padding: 6px 8px;
            }
        """)
        vec_display.setWordWrap(True)
        vector_layout.addWidget(vec_display)
        layout.addWidget(vector_card)

        layout.addStretch()
        return widget

    def create_edit_widget(self):
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        field_style = """
            QLineEdit, QDateEdit {
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                padding: 7px 10px;
                font-size: 13px;
                color: #1E293B;
                background: white;
            }
            QLineEdit:focus, QDateEdit:focus {
                border-color: #3B82F6;
            }
        """

        # Карточка с полями
        edit_card = self._make_info_card()
        edit_layout = QVBoxLayout(edit_card)
        edit_layout.setContentsMargins(16, 14, 16, 14)
        edit_layout.setSpacing(10)

        # ФИО
        edit_layout.addWidget(self._section_label("ФИО"))
        self.edit_full_name = QLineEdit(self.person_data.get('full_name', ''))
        self.edit_full_name.setStyleSheet(field_style)
        edit_layout.addWidget(self.edit_full_name)

        # Дата рождения
        edit_layout.addWidget(self._section_label("ДАТА РОЖДЕНИЯ"))
        self.edit_dob = QDateEdit()
        self.edit_dob.setCalendarPopup(True)
        self.edit_dob.setDisplayFormat("dd.MM.yyyy")
        self.edit_dob.setStyleSheet(field_style)
        dob_str = self.person_data.get('date_of_birth', '')
        if dob_str:
            try:
                dob_date = QDate.fromString(dob_str, "dd.MM.yyyy")
                if dob_date.isValid():
                    self.edit_dob.setDate(dob_date)
                else:
                    self.edit_dob.setDate(QDate.currentDate())
            except Exception:
                self.edit_dob.setDate(QDate.currentDate())
        else:
            self.edit_dob.setDate(QDate.currentDate())
        edit_layout.addWidget(self.edit_dob)

        layout.addWidget(edit_card)

        # Карточка заметок
        notes_card = self._make_info_card()
        notes_layout = QVBoxLayout(notes_card)
        notes_layout.setContentsMargins(16, 12, 16, 12)
        notes_layout.setSpacing(6)
        notes_layout.addWidget(self._section_label("ЗАМЕТКИ"))
        self.edit_notes = QTextEdit(self.person_data.get("notes", ""))
        self.edit_notes.setFixedHeight(72)
        self.edit_notes.setStyleSheet("""
            QTextEdit {
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                padding: 6px 8px;
                font-size: 13px;
                color: #1E293B;
                background: white;
            }
            QTextEdit:focus {
                border-color: #3B82F6;
            }
        """)
        notes_layout.addWidget(self.edit_notes)
        layout.addWidget(notes_card)

        # Инфо о векторе (нередактируемо)
        vec_card = self._make_info_card()
        vec_card_layout = QHBoxLayout(vec_card)
        vec_card_layout.setContentsMargins(16, 12, 16, 12)
        vec_icon = QLabel("🔒")
        vec_icon.setStyleSheet("background: transparent; border: none; font-size: 14px;")
        vec_text_lbl = QLabel(f"Вектор ({len(self.person_data.get('vector_data', []))} элементов) — только для чтения")
        vec_text_lbl.setStyleSheet("""
            QLabel {
                color: #94A3B8;
                font-size: 12px;
                font-style: italic;
                background: transparent;
                border: none;
            }
        """)
        vec_card_layout.addWidget(vec_icon)
        vec_card_layout.addWidget(vec_text_lbl)
        vec_card_layout.addStretch()
        layout.addWidget(vec_card)

        layout.addStretch()
        return widget

    def init_edit_controls(self):
        self.info_stack.setCurrentIndex(0)

    def toggle_edit_mode(self):
        self.is_edit_mode = not self.is_edit_mode

        if self.is_edit_mode:
            self.info_stack.setCurrentIndex(1)
            self.photo_label.setCursor(Qt.PointingHandCursor)

            self.edit_btn.setText("👁  Просмотр")
            self.edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #F59E0B;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 0 12px;
                }
                QPushButton:hover { background-color: #D97706; }
            """)
            self.save_btn.setEnabled(True)
            self.cancel_btn.setEnabled(True)
        else:
            self.info_stack.setCurrentIndex(0)
            self.edit_btn.setText("✏  Редактировать")
            self.edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 0 12px;
                }
                QPushButton:hover { background-color: #2980b9; }
            """)
            self.save_btn.setEnabled(False)
            self.cancel_btn.setEnabled(False)

    def save_changes(self):
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

            self.person_data.update(updated_data)
            self.view_full_name.setText(updated_data['full_name'])
            self.view_dob.setText(updated_data['date_of_birth'])
            self.view_notes.setPlainText(updated_data['notes'])

            if self.save_callback:
                self.save_callback(self.person_data)

            self.toggle_edit_mode()
            QMessageBox.information(self, "Успех", "Данные успешно сохранены!")
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить данные: {e}")

    def cancel_edit(self):
        self.edit_full_name.setText(self.person_data.get('full_name', ''))
        dob_str = self.person_data.get('date_of_birth', '')
        if dob_str:
            try:
                dob_date = QDate.fromString(dob_str, "dd.MM.yyyy")
                if dob_date.isValid():
                    self.edit_dob.setDate(dob_date)
            except ValueError:
                pass
        self.edit_notes.setPlainText(self.person_data.get('notes', ''))
        if self.original_photo_path and os.path.exists(self.original_photo_path):
            self.set_photo(self.original_photo_path)
            self.person_data['photo'] = self.original_photo_path
        self.toggle_edit_mode()

    def set_photo(self, path):
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
                        border: 2px solid #10B981;
                        border-radius: 8px;
                        background-color: #F0FDF4;
                    }
                """)
        except Exception as e:
            print(f"Ошибка загрузки фото: {e}")

    def on_photo_clicked(self, event):
        if not self.is_edit_mode:  # <-- блокируем в режиме просмотра
            return
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.set_photo(file_path)
            # Сразу сохраняем фото в БД
            if self.save_callback:
                self.save_callback(self.person_data)

    def play_audio(self):
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
            from PySide6.QtCore import QUrl
            self.player = QMediaPlayer()
            self.audio_output = QAudioOutput()
            self.player.setAudioOutput(self.audio_output)
            self.player.setSource(QUrl.fromLocalFile(path))
            self.audio_output.setVolume(0.5)
            self.player.play()
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Ошибка", f"Не удалось воспроизвести аудио: {e}")

    def show_full_vector(self):
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QLabel

        dlg = QDialog(self)
        dlg.setWindowTitle(f"Векторные данные — {self.person_data.get('full_name', '')}")
        dlg.setFixedSize(580, 460)
        dlg.setStyleSheet("background-color: #F0F4F8;")

        layout = QVBoxLayout(dlg)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        header = QLabel(f"Вектор · {len(self.person_data.get('vector_data', []))} элементов")
        header.setStyleSheet("font-size: 14px; font-weight: bold; color: #1E293B;")
        layout.addWidget(header)

        vector_data = self.person_data.get("vector_data", [])
        text_edit = QTextEdit()
        text_edit.setPlainText(str(vector_data))
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("""
            QTextEdit {
                font-family: 'Courier New';
                font-size: 10pt;
                background: white;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 8px;
                color: #334155;
            }
        """)
        layout.addWidget(text_edit)

        btn_layout = QHBoxLayout()
        copy_btn = QPushButton("📋  Копировать")
        copy_btn.setFixedHeight(34)
        copy_btn.setCursor(Qt.PointingHandCursor)
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(str(vector_data)))
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                padding: 0 16px;
            }
            QPushButton:hover { background-color: #2563EB; }
        """)
        close_btn = QPushButton("Закрыть")
        close_btn.setFixedHeight(34)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(dlg.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a1f2e;
                color: #94A3B8;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                padding: 0 16px;
            }
            QPushButton:hover { background-color: #2d3447; color: white; }
        """)
        btn_layout.addStretch()
        btn_layout.addWidget(copy_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
        dlg.exec()

    def copy_to_clipboard(self, text):
        from PySide6.QtGui import QGuiApplication
        QGuiApplication.clipboard().setText(text)