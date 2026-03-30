import json
import numpy as np
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSlider, QScrollArea, QGridLayout
)
from PySide6.QtCore import Qt
import config


class AIController:
    def __init__(self, main_controller):
        self.main = main_controller
        self._setup_ui()

    def setup_connections(self):
        pass

    def _setup_ui(self):
        page = self.main.page_ai

        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # ── СЕКЦИЯ ПОРОГОВ ──────────────────────
        thresholds_card = self._make_card()
        thresholds_layout = QVBoxLayout(thresholds_card)
        thresholds_layout.setContentsMargins(16, 14, 16, 14)
        thresholds_layout.setSpacing(10)

        header_row = QHBoxLayout()
        thresholds_title = self._section_label("ПОРОГИ ИДЕНТИФИКАЦИИ")
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
        header_row.addWidget(thresholds_title)
        header_row.addStretch()
        header_row.addWidget(self.save_btn)
        thresholds_layout.addLayout(header_row)

        # Слайдер 1 — высокая уверенность
        self.slider_strong, self.label_strong = self._make_slider(
            "Высокая уверенность", "#10B981",
            int(config.STRONG_THRESHOLD * 100)
        )
        thresholds_layout.addLayout(self._slider_row(
            "Высокая уверенность", self.slider_strong, self.label_strong, "#10B981"
        ))

        # Слайдер 2 — средняя уверенность
        self.slider_weak, self.label_weak = self._make_slider(
            "Средняя уверенность", "#F59E0B",
            int(config.WEAK_THRESHOLD * 100)
        )
        thresholds_layout.addLayout(self._slider_row(
            "Средняя уверенность", self.slider_weak, self.label_weak, "#F59E0B"
        ))

        # Слайдер 3 — минимальный порог
        self.slider_min, self.label_min = self._make_slider(
            "Минимальный порог", "#EF4444",
            int(config.MIN_SIMILARITY * 100)
        )
        thresholds_layout.addLayout(self._slider_row(
            "Минимальный порог", self.slider_min, self.label_min, "#EF4444"
        ))

        main_layout.addWidget(thresholds_card)

        # ── СЕКЦИЯ МАТРИЦЫ ───────────────────────
        matrix_card = self._make_card()
        matrix_layout = QVBoxLayout(matrix_card)
        matrix_layout.setContentsMargins(16, 14, 16, 14)
        matrix_layout.setSpacing(10)

        matrix_header_row = QHBoxLayout()
        matrix_title = self._section_label("МАТРИЦА СХОЖЕСТИ")
        self.refresh_btn = QPushButton("Обновить")
        self.refresh_btn.setFixedSize(100, 28)
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
        matrix_header_row.addWidget(matrix_title)
        matrix_header_row.addStretch()
        matrix_header_row.addWidget(self.refresh_btn)
        matrix_layout.addLayout(matrix_header_row)

        # Легенда
        legend_row = QHBoxLayout()
        for color, text in [("#10B981", "≥ 0.72 высокая"), ("#F59E0B", "0.65–0.72 средняя"), ("#EF4444", "< 0.65 низкая")]:
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {color}; font-size: 13px;")
            lbl = QLabel(text)
            lbl.setStyleSheet("color: #64748b; font-size: 11px;")
            legend_row.addWidget(dot)
            legend_row.addWidget(lbl)
            legend_row.addSpacing(12)
        legend_row.addStretch()
        matrix_layout.addLayout(legend_row)

        # Скролл для матрицы
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        self.matrix_widget = QWidget()
        self.matrix_widget.setStyleSheet("background: transparent;")
        self.matrix_inner = QGridLayout(self.matrix_widget)
        self.matrix_inner.setSpacing(3)

        scroll.setWidget(self.matrix_widget)
        matrix_layout.addWidget(scroll)

        main_layout.addWidget(matrix_card)

        # Строим матрицу при открытии
        self._build_matrix()

    def _make_slider(self, name, color, value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)
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
        from PySide6.QtWidgets import QMessageBox
        try:
            strong = self.slider_strong.value() / 100
            weak = self.slider_weak.value() / 100
            min_sim = self.slider_min.value() / 100

            # Валидация порядка
            if not (strong > weak > min_sim):
                QMessageBox.warning(
                    self.main, "Ошибка",
                    "Пороги должны быть в порядке:\nВысокая > Средняя > Минимальная"
                )
                return

            # Читаем config.py и перезаписываем значения
            config_path = "config.py"
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read()

            import re
            content = re.sub(r"STRONG_THRESHOLD\s*=\s*[\d.]+", f"STRONG_THRESHOLD = {strong}", content)
            content = re.sub(r"WEAK_THRESHOLD\s*=\s*[\d.]+", f"WEAK_THRESHOLD = {weak}", content)
            content = re.sub(r"MIN_SIMILARITY\s*=\s*[\d.]+", f"MIN_SIMILARITY = {min_sim}", content)

            with open(config_path, "w", encoding="utf-8") as f:
                f.write(content)

            # Обновляем значения в памяти
            config.STRONG_THRESHOLD = strong
            config.WEAK_THRESHOLD = weak
            config.MIN_SIMILARITY = min_sim

            QMessageBox.information(self.main, "Успех", "Пороги сохранены!")

        except Exception as e:
            QMessageBox.critical(self.main, "Ошибка", f"Не удалось сохранить: {e}")

    def _build_matrix(self):
        # Очищаем старую матрицу
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

            names = [p["full_name"].split()[0] for p in people]  # только имя
            vectors = [np.array(p["vector_data"]) for p in people]
            n = len(people)

            # Заголовки столбцов
            for j, name in enumerate(names):
                lbl = QLabel(name)
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setStyleSheet("color: #64748b; font-size: 10px;")
                lbl.setFixedWidth(70)
                self.matrix_inner.addWidget(lbl, 0, j + 1)

            for i in range(n):
                # Заголовок строки
                row_lbl = QLabel(names[i])
                row_lbl.setStyleSheet("color: #64748b; font-size: 10px;")
                row_lbl.setFixedWidth(60)
                self.matrix_inner.addWidget(row_lbl, i + 1, 0)

                for j in range(n):
                    score = self._cosine_similarity(vectors[i], vectors[j])

                    # Цвет ячейки
                    if score >= config.STRONG_THRESHOLD:
                        bg, fg = "#d1fae5", "#065f46"
                    elif score >= config.WEAK_THRESHOLD:
                        bg, fg = "#fef3c7", "#78350f"
                    else:
                        bg, fg = "#fee2e2", "#7f1d1d"

                    cell = QLabel(f"{score:.2f}")
                    cell.setAlignment(Qt.AlignCenter)
                    cell.setFixedSize(70, 24)
                    cell.setStyleSheet(f"""
                        QLabel {{
                            background: {bg};
                            color: {fg};
                            border-radius: 4px;
                            font-size: 11px;
                            font-weight: bold;
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