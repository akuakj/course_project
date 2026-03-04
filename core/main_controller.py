from PySide6.QtWidgets import QMainWindow
from gui.main_window import Ui_MainWindow
from core.analysis_controller import AnalysisController
from core.database_controller import DatabaseController
from core.ai_controller import AIController


class MainController(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("VoiceMaxxing")
        self.setFixedSize(810, 490)

        # Инициализация контроллеров
        self.analysis_controller = AnalysisController(self)
        self.database_controller = DatabaseController(self)
        self.ai_controller = AIController(self)

        self.setup_connections()
        self._setup_home_page()

        self.stackedWidget.setCurrentIndex(0)

    def _setup_home_page(self):
        """Перестраивает стартовую страницу через QWebEngineView"""
        from PySide6.QtWebEngineWidgets import QWebEngineView
        from PySide6.QtWidgets import QVBoxLayout, QWidget

        for child in self.page_start.findChildren(QWidget):
            child.deleteLater()

        # Статус БД
        try:
            stats = self.database_controller.db_manager.get_statistics()
            db_count = stats["total_records"]
            db_status = "Подключена"
            db_color = "#27AE60"
        except Exception:
            db_count = 0
            db_status = "Ошибка"
            db_color = "#E74C3C"

        # Статус микрофона
        try:
            import sounddevice as sd
            sd.query_devices()
            mic_status = "Доступен"
            mic_color = "#27AE60"
        except Exception:
            mic_status = "Недоступен"
            mic_color = "#E74C3C"

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        font-family: 'Segoe UI', sans-serif;
        background-color: #F0F8FF;
        padding: 24px;
        color: #2C3E50;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100vh;
    }}
    .title {{
        font-size: 20px;
        font-weight: 700;
        color: #2C3E50;
        line-height: 1.3;
        margin-bottom: 8px;
    }}
    .subtitle {{
        font-size: 14px;
        color: #7F8C8D;
        margin-bottom: 20px;
        line-height: 1.5;
    }}
    .cards {{
        display: flex;
        gap: 12px;
    }}
    .card {{
        flex: 1;
        background: white;
        border: 1px solid #EAECEE;
        border-radius: 8px;
        padding: 12px 14px;
        border-left: 4px solid #ccc;
    }}
    .card-label {{
        font-size: 11px;
        color: #BDC3C7;
        font-weight: 600;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .card-value {{
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 2px;
    }}
    .card-desc {{
        font-size: 11px;
        color: #BDC3C7;
    }}
    .divider {{
        border: none;
        border-top: 1px solid #EAECEE;
        margin-bottom: 16px;
    }}
    .section-title {{
        font-size: 12px;
        font-weight: 700;
        color: #7F8C8D;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 12px;
    }}
    .features {{
        display: flex;
        gap: 12px;
    }}
    .feature {{
        flex: 1;
        background: white;
        border: 1px solid #EAECEE;
        border-radius: 8px;
        padding: 12px 14px;
    }}
    .feature-title {{
        font-size: 13px;
        font-weight: 700;
        color: #2C3E50;
        margin-bottom: 6px;
    }}
    .feature-desc {{
        font-size: 11px;
        color: #95A5A6;
        line-height: 1.5;
    }}
</style>
</head>
<body>

    <!-- Верхняя часть: заголовок + карточки статуса -->
    <div>
        <div class="title">Система идентификации личности<br>по голосовому биометрическому признаку</div>
        <div class="subtitle">
            Приложение предназначено для анализа и идентификации голосовых данных
            с использованием нейросетевых алгоритмов машинного обучения.
        </div>
        <div class="cards">
            <div class="card" style="border-left-color: {db_color};">
                <div class="card-label">База данных</div>
                <div class="card-value" style="color: {db_color};">{db_status}</div>
                <div class="card-desc">Записей: {db_count}</div>
            </div>
            <div class="card" style="border-left-color: #27AE60;">
                <div class="card-label">Модель</div>
                <div class="card-value" style="color: #27AE60;">Загружена</div>
                <div class="card-desc">Resemblyzer (GE2E)</div>
            </div>
            <div class="card" style="border-left-color: {mic_color};">
                <div class="card-label">Микрофон</div>
                <div class="card-value" style="color: {mic_color};">{mic_status}</div>
                <div class="card-desc">Входное устройство</div>
            </div>
        </div>
    </div>

    <!-- Нижняя часть: возможности системы -->
    <div>
        <hr class="divider">
        <div class="section-title">Возможности системы</div>
        <div class="features">
            <div class="feature">
                <div class="feature-title">Идентификация</div>
                <div class="feature-desc">Определение личности по голосовому фрагменту из базы данных</div>
            </div>
            <div class="feature">
                <div class="feature-title">База голосов</div>
                <div class="feature-desc">Хранение и управление голосовыми биометрическими профилями</div>
            </div>
            <div class="feature">
                <div class="feature-title">Запись</div>
                <div class="feature-desc">Захват голоса в реальном времени через микрофон</div>
            </div>
        </div>
    </div>

</body>
</html>"""

        layout = QVBoxLayout(self.page_start)
        layout.setContentsMargins(0, 0, 0, 0)

        self.web_view = QWebEngineView()
        self.web_view.setHtml(html)
        layout.addWidget(self.web_view)

    def setup_connections(self):
        """Подключение всех кнопок"""
        self.btn_home.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.btn_analyze.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btn_database.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.btn_ai.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))

        self.analysis_controller.setup_connections()
        self.database_controller.setup_connections()
        self.ai_controller.setup_connections()