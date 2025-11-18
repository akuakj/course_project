from PySide6.QtWidgets import QTableWidgetItem, QMessageBox, QHeaderView
from PySide6.QtCore import Qt
from datetime import datetime
from .db_manager import TinyDBVoiceManager


class DatabaseController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.db_manager = TinyDBVoiceManager()

    def setup_connections(self):
        """Подключение кнопок базы данных"""
        self.main.btn_refresh_db.clicked.connect(self.refresh_database)
        self.main.btn_delete_record.clicked.connect(self.delete_selected_record)
        self.main.btn_search_text.clicked.connect(self.search_in_database)

        # Автоматически обновляем при переходе на вкладку
        self.main.btn_database.clicked.connect(self.refresh_database)

    def refresh_database(self):
        """Обновление таблицы базы данных"""
        try:
            # Получаем все записи из БД
            all_people = self.db_manager.get_all_people()

            # Настраиваем таблицу
            table = self.main.table_voices
            table.setRowCount(len(all_people))

            # Заполняем таблицу данными
            for row, person in enumerate(all_people):
                # ID (обрезаем для отображения)
                short_id = person['id'][:8] + "..."
                table.setItem(row, 0, QTableWidgetItem(short_id))
                table.setItem(row, 0, QTableWidgetItem(person['id']))  # Полный ID в данных

                # ФИО
                table.setItem(row, 1, QTableWidgetItem(person['full_name']))

                # Дата добавления (форматируем)
                created_date = person['created_at']
                if 'T' in created_date:
                    date_part = created_date.split('T')[0]
                    time_part = created_date.split('T')[1][:8]
                    formatted_date = f"{date_part} {time_part}"
                else:
                    formatted_date = created_date
                table.setItem(row, 2, QTableWidgetItem(formatted_date))

                # Биометрические данные (информация о векторе)
                vector_info = f"Вектор: {len(person['vector_data'])}D"
                if person.get('notes'):
                    vector_info += f" | {person['notes']}"
                table.setItem(row, 3, QTableWidgetItem(vector_info))

            # Настраиваем заголовки таблицы
            header = table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # ФИО
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Дата
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Био данные

            # Обновляем статистику
            self.update_statistics()

            print(f"База данных обновлена: {len(all_people)} записей")

        except Exception as e:
            print(f"Ошибка обновления базы данных: {e}")
            QMessageBox.warning(self.main, "Ошибка", f"Не удалось загрузить базу данных: {e}")

    def update_statistics(self):
        """Обновление статистики базы данных"""
        try:
            stats = self.db_manager.get_statistics()

            self.main.label_total_records.setText(f"Всего записей: {stats['total_records']}")
            self.main.label_last_update.setText(f"Последнее обновление: {stats['last_update']}")

            # Обновляем статус БД
            if stats['total_records'] > 0:
                self.main.label_db_status.setText("Статус БД: ✅ OK")
                self.main.label_db_status.setStyleSheet("""
                    QLabel {
                        color: #27AE60;
                        font-weight: bold;
                        padding: 5px 10px;
                        background-color: #EAFAEE;
                        border: 1px solid #27AE60;
                        border-radius: 3px;
                    }
                """)
            else:
                self.main.label_db_status.setText("Статус БД: ⚠️ Пусто")
                self.main.label_db_status.setStyleSheet("""
                    QLabel {
                        color: #F39C12;
                        font-weight: bold;
                        padding: 5px 10px;
                        background-color: #FEF9E7;
                        border: 1px solid #F39C12;
                        border-radius: 3px;
                    }
                """)

        except Exception as e:
            print(f"Ошибка обновления статистики: {e}")

    def delete_selected_record(self):
        """Удаление выбранной записи"""
        try:
            table = self.main.table_voices
            selected_rows = table.selectionModel().selectedRows()

            if not selected_rows:
                QMessageBox.information(self.main, "Информация", "Выберите запись для удаления")
                return

            selected_row = selected_rows[0].row()
            person_id = table.item(selected_row, 0).text()  # Получаем полный ID

            # Подтверждение удаления
            reply = QMessageBox.question(
                self.main,
                "Подтверждение удаления",
                "Вы уверены, что хотите удалить эту запись?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                success = self.db_manager.delete_person(person_id)
                if success:
                    QMessageBox.information(self.main, "Успех", "Запись успешно удалена")
                    self.refresh_database()
                else:
                    QMessageBox.warning(self.main, "Ошибка", "Не удалось удалить запись")

        except Exception as e:
            print(f"Ошибка удаления записи: {e}")
            QMessageBox.warning(self.main, "Ошибка", f"Ошибка при удалении: {e}")

    def search_in_database(self):
        """Поиск по базе данных"""
        try:
            search_text = self.main.lineEdit_search.text().strip().lower()

            if not search_text:
                self.refresh_database()  # Показываем все если поиск пустой
                return

            all_people = self.db_manager.get_all_people()
            filtered_people = []

            for person in all_people:
                # Ищем в ФИО и заметках
                if (search_text in person['full_name'].lower() or
                        search_text in person.get('notes', '').lower()):
                    filtered_people.append(person)

            # Обновляем таблицу с результатами поиска
            table = self.main.table_voices
            table.setRowCount(len(filtered_people))

            for row, person in enumerate(filtered_people):
                short_id = person['id'][:8] + "..."
                table.setItem(row, 0, QTableWidgetItem(short_id))
                table.setItem(row, 0, QTableWidgetItem(person['id']))
                table.setItem(row, 1, QTableWidgetItem(person['full_name']))

                # Дата
                created_date = person['created_at']
                if 'T' in created_date:
                    date_part = created_date.split('T')[0]
                    formatted_date = date_part
                else:
                    formatted_date = created_date
                table.setItem(row, 2, QTableWidgetItem(formatted_date))

                # Био данные
                vector_info = f"Вектор: {len(person['vector_data'])}D"
                if person.get('notes'):
                    vector_info += f" | {person['notes']}"
                table.setItem(row, 3, QTableWidgetItem(vector_info))

            # Обновляем статистику для поиска
            self.main.label_total_records.setText(f"Найдено записей: {len(filtered_people)}")

            if not filtered_people:
                QMessageBox.information(self.main, "Поиск", "Записи не найдены")

        except Exception as e:
            print(f"Ошибка поиска: {e}")
            QMessageBox.warning(self.main, "Ошибка", f"Ошибка при поиске: {e}")

    def get_selected_person_id(self):
        """Получение ID выбранного человека"""
        table = self.main.table_voices
        selected_rows = table.selectionModel().selectedRows()

        if selected_rows:
            selected_row = selected_rows[0].row()
            return table.item(selected_row, 0).text()  # Полный ID
        return None