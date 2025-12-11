from PySide6.QtWidgets import QTableWidgetItem, QMessageBox, QHeaderView
from PySide6.QtCore import Qt
from datetime import datetime
from .db_manager import TinyDBVoiceManager

# Импортируем диалог с подробностями
from .person_details_dialog import PersonDetailsDialog

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
        # Двойной клик по строке открывает подробности
        self.main.table_voices.cellDoubleClicked.connect(self.open_person_details)

    def refresh_database(self):
        """Обновление таблицы базы данных (только ФИО и Дата добавления)"""
        try:
            all_people = self.db_manager.get_all_people()
            table = self.main.table_voices
            table.setRowCount(len(all_people))
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["ФИО", "Дата добавления"])

            for row, person in enumerate(all_people):
                table.setItem(row, 0, QTableWidgetItem(person['full_name']))
                created_date = person['created_at'].split('T')[0]  # дата без времени
                table.setItem(row, 1, QTableWidgetItem(created_date))

            header = table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # ФИО растягивается
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Дата по содержимому

            self.update_statistics()
            print(f"База данных обновлена: {len(all_people)} записей")

        except Exception as e:
            print(f"Ошибка обновления базы данных: {e}")
            QMessageBox.warning(self.main, "Ошибка", f"Не удалось загрузить базу данных: {e}")

    def open_person_details(self, row, column):
        """Открытие окна с полной информацией о человеке"""
        person_id = self.get_person_id_by_row(row)
        person_data = self.db_manager.get_person_by_id(person_id)
        if person_data:
            dlg = PersonDetailsDialog(
                person_data,
                save_callback=self.save_person_data  # ← вот это главное
            )
            dlg.exec()

    def save_person_data(self, updated_person):
        """Сохранение изменённых данных человека (включая фото)"""
        try:
            person_id = updated_person["id"]
            self.db_manager.update_person(person_id, updated_person)
            print(f"[OK] Данные пользователя {person_id} обновлены")

            # Обновить таблицу, если нужно
            self.refresh_database()

        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")


    def get_person_id_by_row(self, row):
        """Получение ID человека по выбранной строке"""
        table = self.main.table_voices
        full_name = table.item(row, 0).text()
        person = self.db_manager.get_person_by_name(full_name)
        return person[0]['id'] if person else None

    def update_statistics(self):
        """Обновление статистики базы данных"""
        try:
            stats = self.db_manager.get_statistics()
            self.main.label_total_records.setText(f"Всего записей: {stats['total_records']}")
            self.main.label_last_update.setText(f"Последнее обновление: {stats['last_update']}")
            if stats['total_records'] > 0:
                self.main.label_db_status.setText("Статус БД: ✅ OK")
                self.main.label_db_status.setStyleSheet(
                    "color: #27AE60; font-weight: bold; padding: 5px 10px;"
                    "background-color: #EAFAEE; border: 1px solid #27AE60; border-radius: 3px;"
                )
            else:
                self.main.label_db_status.setText("Статус БД: ⚠️ Пусто")
                self.main.label_db_status.setStyleSheet(
                    "color: #F39C12; font-weight: bold; padding: 5px 10px;"
                    "background-color: #FEF9E7; border: 1px solid #F39C12; border-radius: 3px;"
                )
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
            person_id = self.get_person_id_by_row(selected_row)

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
                self.refresh_database()
                return

            all_people = self.db_manager.get_all_people()
            filtered_people = [p for p in all_people if search_text in p['full_name'].lower()
                               or search_text in p.get('notes', '').lower()]

            table = self.main.table_voices
            table.setRowCount(len(filtered_people))
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["ФИО", "Дата добавления"])

            for row, person in enumerate(filtered_people):
                table.setItem(row, 0, QTableWidgetItem(person['full_name']))
                created_date = person['created_at'].split('T')[0]
                table.setItem(row, 1, QTableWidgetItem(created_date))

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
            return self.get_person_id_by_row(selected_rows[0].row())
        return None
