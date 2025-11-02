class DatabaseController:
    def __init__(self, main_controller):
        self.main = main_controller

    def setup_connections(self):
        """Подключение кнопок базы данных"""
        # Кнопки управления БД
        self.main.btn_refresh_db.clicked.connect(self.refresh_database)
        self.main.btn_delete_record.clicked.connect(self.delete_record)
        self.main.btn_search_text.clicked.connect(self.search_database)

    def refresh_database(self):
        """Обновление базы данных"""
        print("Обновление БД...")

    def delete_record(self):
        """Удаление записи"""
        print("Удаление записи...")


    def search_database(self):
        """Поиск в базе данных"""
        search_text = self.main.lineEdit_search.text()
        print(f"Поиск: {search_text}")
