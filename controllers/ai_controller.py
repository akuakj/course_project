import numpy as np
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSlider, QScrollArea,
    QGridLayout, QMessageBox
)
from PySide6.QtCore import Qt
from services.settings_manager import (
    save_thresholds, get_thresholds,
    get_encoder_type, save_encoder_type
)
from services.encoder_factory import get_available_encoders
import config

#  Контроллер страницы "Нейросеть"
class AIController:
    def __init__(self, main_controller):
        self.main = main_controller
        # self._rebuild_thread = None
        self._setup_ui()

    def setup_connections(self):
        pass

    def _setup_ui(self):
        page = self.main.page_ai

        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(10, 6, 10, 6)
        main_layout.setSpacing(6)

        # Секция выбора модели
        model_card = self._make_card()
        model_layout = QVBoxLayout(model_card)
        model_layout.setContentsMargins(16, 10, 16, 10)
        model_layout.setSpacing(8)
    
        model_layout.addWidget(self._section_label("МОДЕЛЬ ЭНКОДЕРА"))

        controls_row = QHBoxLayout()
        controls_row.setSpacing(8)

        from PySide6.QtWidgets import QComboBox
        self.encoder_combo = QComboBox()
        self.encoder_combo.setFixedHeight(32)
        self.encoder_combo.setStyleSheet("""
            QComboBox {
                border: none;
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 12px;
                font-weight: bold;
                color: #1E293B;
                background: #F1F5F9;
            }
            QComboBox:hover { background: #E2E8F0; }
            QComboBox::drop-down { border: none; width: 24px; }
            QComboBox QAbstractItemView {
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                background: white;
                selection-background-color: #EFF6FF;
                selection-color: #1E293B;
            }
        """)

        encoders = get_available_encoders()
        current_encoder = get_encoder_type()
        for encoder_id, info in encoders.items():
            self.encoder_combo.addItem(info["display_name"], encoder_id)
            if encoder_id == current_encoder:
                self.encoder_combo.setCurrentIndex(self.encoder_combo.count() - 1)

        self.apply_model_btn = QPushButton("Применить")
        self.apply_model_btn.setFixedSize(100, 32)
        self.apply_model_btn.setCursor(Qt.PointingHandCursor)
        self.apply_model_btn.clicked.connect(self._apply_encoder)
        self.apply_model_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6; color: white;
                border: none; border-radius: 6px;
                font-size: 11px; font-weight: bold;
            }
            QPushButton:hover { background-color: #2563EB; }
            QPushButton:disabled { background-color: #E2E8F0; color: #94A3B8; }
        """)

        controls_row.addWidget(self.encoder_combo, stretch=1)
        controls_row.addWidget(self.apply_model_btn)
        model_layout.addLayout(controls_row)

        # Статус пересборки — скрыт по умолчанию
        self.rebuild_status_lbl = QLabel("")
        self.rebuild_status_lbl.setStyleSheet("""
            QLabel {
                color: #3B82F6; font-size: 11px;
                background: #EFF6FF;
                border-radius: 4px;
                padding: 4px 8px;
            }
        """)
        self.rebuild_status_lbl.hide()
        model_layout.addWidget(self.rebuild_status_lbl)

        main_layout.addWidget(model_card)


        # секция порогов
        thresholds_card = self._make_card()
        thresholds_layout = QVBoxLayout(thresholds_card)
        thresholds_layout.setContentsMargins(16, 10, 16, 10)
        thresholds_layout.setSpacing(7)

        header_row = QHBoxLayout()
        header_row.addWidget(self._section_label("ПОРОГИ ИДЕНТИФИКАЦИИ"))
        header_row.addStretch()
        self.save_btn = QPushButton("Сохранить")
        self.save_btn.setFixedSize(100, 28)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self._save_thresholds)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB; color: white;
                border: none; border-radius: 5px;
                font-size: 11px; font-weight: bold;
            }
            QPushButton:hover { background-color: #2980B9; }
        """)
        header_row.addWidget(self.save_btn)
        thresholds_layout.addLayout(header_row)

        self.slider_strong, self.label_strong = self._make_slider(
            "Высокая уверенность", "#10B981",
            int(config.STRONG_THRESHOLD * 100)
        )
        thresholds_layout.addLayout(self._slider_row(
            "Высокая уверенность", self.slider_strong, self.label_strong, "#10B981"
        ))

        self.slider_weak, self.label_weak = self._make_slider(
            "Средняя уверенность", "#F59E0B",
            int(config.WEAK_THRESHOLD * 100)
        )
        thresholds_layout.addLayout(self._slider_row(
            "Средняя уверенность", self.slider_weak, self.label_weak, "#F59E0B"
        ))

        self.slider_min, self.label_min = self._make_slider(
            "Минимальный порог", "#EF4444",
            int(config.MIN_SIMILARITY * 100)
        )
        thresholds_layout.addLayout(self._slider_row(
            "Минимальный порог", self.slider_min, self.label_min, "#EF4444"
        ))

        main_layout.addWidget(thresholds_card)

        # секция матрицы
        matrix_card = self._make_card()
        matrix_layout = QVBoxLayout(matrix_card)
        matrix_layout.setContentsMargins(16, 10, 16, 10)
        matrix_layout.setSpacing(7)

        matrix_header_row = QHBoxLayout()
        matrix_header_row.addWidget(self._section_label("МАТРИЦА СХОЖЕСТИ"))
        matrix_header_row.addStretch()
        self.refresh_btn = QPushButton("Обновить")
        self.refresh_btn.setFixedSize(130, 28)
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.clicked.connect(self._build_matrix)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8fafc; color: #475569;
                border: 1px solid #e2e8f0; border-radius: 5px;
                font-size: 11px; font-weight: bold;
            }
            QPushButton:hover { background-color: #e2e8f0; }
        """)
        matrix_header_row.addWidget(self.refresh_btn)
        matrix_layout.addLayout(matrix_header_row)

        strong, weak, _ = get_thresholds()
        legend_row = QHBoxLayout()
        for color, text in [
            ("#10B981", f"≥ {strong:.2f} высокая"),
            ("#F59E0B", f"{weak:.2f}–{strong:.2f} средняя"),
            ("#EF4444", f"< {weak:.2f} низкая")
        ]:
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {color}; font-size: 13px; border: none; background: transparent;")
            lbl = QLabel(text)
            lbl.setStyleSheet("color: #64748b; font-size: 11px; border: none; background: transparent;")
            legend_row.addWidget(dot)
            legend_row.addWidget(lbl)
            legend_row.addSpacing(12)
        legend_row.addStretch()
        matrix_layout.addLayout(legend_row)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.matrix_widget = QWidget()
        self.matrix_widget.setStyleSheet("background: transparent;")
        self.matrix_inner = QGridLayout(self.matrix_widget)
        self.matrix_inner.setSpacing(3)

        scroll.setWidget(self.matrix_widget)
        matrix_layout.addWidget(scroll)
        main_layout.addWidget(matrix_card)

        self._build_matrix()

    # выбор и применение модели
    def _get_selected_encoder_id(self) -> str:
        """Возвращает ID энкодера из выпадающего списка."""
        return self.encoder_combo.currentData()

    def _apply_encoder(self):
        selected_id = self._get_selected_encoder_id()
        current_id = get_encoder_type()

        if selected_id == current_id:
            encoders = get_available_encoders()
            QMessageBox.information(
                self.main,
                "Модель уже активна",
                f"Модель «{encoders[selected_id]['display_name']}» уже используется."
            )
            return

        encoders = get_available_encoders()
        display_name = encoders[selected_id]["display_name"]

        reply = QMessageBox.question(
            self.main,
            "Смена модели",
            f"Выбрана модель: {display_name}\n\n"
            "Для применения необходимо пересчитать голосовые векторы.\n\n"
            "Это может занять несколько минут при следующем запуске.\n"
            "Приложение будет перезапущено.\n\n"
            "Продолжить?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            for i in range(self.encoder_combo.count()):
                if self.encoder_combo.itemData(i) == current_id:
                    self.encoder_combo.setCurrentIndex(i)
                    break
            return

        # сохраняем выбор и сразу перезапускаемся
        save_encoder_type(selected_id)

        # помечаем, что нужна пересборка при следующем старте
        from services.settings_manager import load_settings, save_settings
        settings = load_settings()
        settings["rebuild_needed"] = True
        save_settings(settings)

        import sys, subprocess
        subprocess.Popen([sys.executable] + sys.argv)
        self.main.close()

    # пороги
    def _make_slider(self, name, color, value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setFixedHeight(20)

        slider.setValue(value)
        slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 4px; background: #e2e8f0; border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                width: 16px; height: 16px; margin: -6px 0;
                background: white; border: 2px solid {color};
                border-radius: 8px;
            }}
            QSlider::sub-page:horizontal {{
                background: {color}; border-radius: 2px;
            }}
        """)
        label = QLabel(f"{value / 100:.2f}")
        label.setFixedWidth(36)
        label.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: bold;")
        slider.valueChanged.connect(lambda v, l=label: l.setText(f"{v / 100:.2f}"))
        return slider, label

    def _slider_row(self, title, slider, label, color):
        row = QHBoxLayout()
        name_lbl = QLabel(title)
        name_lbl.setFixedWidth(160)
        name_lbl.setStyleSheet("color: #475569; font-size: 11px;")
        row.addWidget(name_lbl)
        row.addWidget(slider)
        row.addWidget(label)
        return row

    def _save_thresholds(self):
        try:
            strong = self.slider_strong.value() / 100
            weak = self.slider_weak.value() / 100
            min_sim = self.slider_min.value() / 100

            if not (strong > weak > min_sim):
                QMessageBox.warning(
                    self.main, "Ошибка",
                    "Пороги должны быть в порядке:\nВысокая > Средняя > Минимальная"
                )
                return

            if not save_thresholds(strong, weak, min_sim):
                QMessageBox.critical(self.main, "Ошибка", "Не удалось сохранить настройки")
                return

            config.STRONG_THRESHOLD = strong
            config.WEAK_THRESHOLD = weak
            config.MIN_SIMILARITY = min_sim

            QMessageBox.information(self.main, "Успех", "Пороги сохранены!")

        except Exception as e:
            QMessageBox.critical(self.main, "Ошибка", f"Не удалось сохранить: {e}")

    # матрица схожести
    def _build_matrix(self):
        while self.matrix_inner.count():
            item = self.matrix_inner.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            people = self.main.db_manager.get_all_people()
            if not people:
                lbl = QLabel("База данных пуста")
                lbl.setStyleSheet("color: #94a3b8; font-size: 12px;")
                self.matrix_inner.addWidget(lbl, 0, 0)
                return

            names = [p["full_name"].split()[0] for p in people]
            vectors = [np.array(p["vector_data"]) for p in people]
            n = len(people)

            CELL_W = 52   # ширина ячейки
            CELL_H = 24   # высота ячейки
            ROW_LBL_W = 55  # ширина подписи строки

            # заголовки столбцов
            for j, name in enumerate(names):
                lbl = QLabel(name[:7])
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setFixedSize(CELL_W, 20)
                lbl.setStyleSheet("color: R64748b; font-size: 10px; border: none; background: transparent;")
                self.matrix_inner.addWidget(lbl, 0, j + 1)

            # строки
            for i in range(n):
                row_lbl = QLabel(names[i][:7])
                row_lbl.setAlignment(Qt.AlignVCenter)
                row_lbl.setFixedSize(ROW_LBL_W, CELL_H)
                row_lbl.setStyleSheet("color: #64748b; font-size: 10px; border: none; background: transparent;")
                self.matrix_inner.addWidget(row_lbl, i + 1, 0)

                for j in range(n):
                    score = self._cosine_similarity(vectors[i], vectors[j])

                    if score >= config.STRONG_THRESHOLD:
                        bg, fg = "#d1fae5", "#065f46"
                    elif score >= config.WEAK_THRESHOLD:
                        bg, fg = "#fef3c7", "#78350f"
                    else:
                        bg, fg = "#fee2e2", "#7f1d1d"

                    cell = QLabel(f"{score:.2f}")
                    cell.setAlignment(Qt.AlignCenter)
                    cell.setFixedSize(CELL_W, CELL_H)
                    cell.setStyleSheet(f"""
                        QLabel {{
                            background: {bg}; color: {fg};
                            border-radius: 4px;
                            font-size: 11px; font-weight: bold;
                        }}
                    """)
                    self.matrix_inner.addWidget(cell, i + 1, j + 1)

        except Exception as e:
            print(f"Ошибка построения матрицы: {e}")

    def _cosine_similarity(self, a, b):
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))


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