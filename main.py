import sys
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

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