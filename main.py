import sys
import os
from PySide6.QtWidgets import QApplication
from controllers.main_controller import MainController


sys.path.append(os.path.join(os.path.dirname(__file__), 'gui'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))




def main():
    app = QApplication(sys.argv)

    # Создаем главный контроллер
    controller = MainController()
    controller.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()