from PySide6.QtWidgets import QMainWindow
from gui.main_window import Ui_MainWindow
from core.analysis_controller import AnalysisController
from core.database_controller import DatabaseController
from core.ai_controller import AIController


class MainController(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Настройка окна
        self.setWindowTitle("VoiceMaxxing")
        self.setFixedSize(810, 490)

        # Инициализация контроллеров
        self.analysis_controller = AnalysisController(self)
        self.database_controller = DatabaseController(self)
        self.ai_controller = AIController(self)

        # Подключаем кнопки
        self.setup_connections()

        # Показываем первую страницу
        self.stackedWidget.setCurrentIndex(0)

    def setup_connections(self):
        """Подключение всех кнопок"""
        # Меню навигации
        self.btn_home.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.btn_analyze.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btn_database.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.btn_ai.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))

        # Кнопка перехода со стартовой страницы
        self.btn_start.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        # Подключаем логику анализа
        self.analysis_controller.setup_connections()

        # Подключаем логику базы данных
        self.database_controller.setup_connections()

        # Подключаем логику нейросети
        self.ai_controller.setup_connections()