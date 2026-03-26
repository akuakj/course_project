from PySide6.QtWidgets import QMessageBox, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QObject, Slot
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from datetime import datetime
from .db_manager import TinyDBVoiceManager
from .person_details_dialog import PersonDetailsDialog
from add_person_dialog import AddPersonDialog



#  Мост между JavaScript и Python
class TableBridge(QObject):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    @Slot(str)
    def on_row_click(self, person_id):
        """Одиночный клик — запоминаем выбранную запись"""
        self.controller.selected_person_id = person_id

    @Slot(str)
    def on_row_double_click(self, person_id):
        """Двойной клик — открываем детали"""
        self.controller.selected_person_id = person_id
        self.controller._open_details_by_id(person_id)



#  Контроллер базы данных
class DatabaseController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.db_manager = TinyDBVoiceManager()
        self.selected_person_id = None
        self._all_people = []

        self._setup_web_table()

    def _setup_web_table(self):
        """Создаём QWebEngineView на месте таблицы"""
        page = self.main.page_database

        self.web_view = QWebEngineView(page)
        self.web_view.setGeometry(10, 140, 601, 265)

        # Настраиваем QWebChannel
        self.channel = QWebChannel()
        self.bridge = TableBridge(self)
        self.channel.registerObject("bridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

        self._render_table([])

    def _render_table(self, people):
        """Рендерим HTML таблицу"""
        rows_html = ""
        for i, person in enumerate(people):
            created_date = person['created_at'].split('T')[0]
            person_id = person['id']
            bg = "white" if i % 2 == 0 else "#F8F9F9"
            rows_html += f"""
                <tr data-id="{person_id}"
                    style="background: {bg};"
                    onclick="handleClick('{person_id}')"
                    ondblclick="handleDblClick('{person_id}')">
                    <td style="width: 60px; text-align: center; color: #BDC3C7;">{i + 1}</td>
                    <td>{person['full_name']}</td>
                    <td style="width: 130px; text-align: center; color: #7F8C8D;">{created_date}</td>
                </tr>
            """

        if not rows_html:
            rows_html = """
                <tr>
                    <td colspan="3" style="text-align: center; color: #BDC3C7; padding: 30px;">
                        База данных пуста
                    </td>
                </tr>
            """

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="qrc:///qtwebchannel/qwebchannel.js"></script>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        font-family: 'Segoe UI', sans-serif;
        background: white;
        overflow-x: hidden;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
    }}
    thead tr {{
        background-color: #34495E;
        color: white;
        position: sticky;
        top: 0;
        z-index: 10;
    }}
    thead td {{
        padding: 10px 12px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    tbody tr {{
        cursor: pointer;
        transition: background 0.15s;
        border-bottom: 1px solid #EAECEE;
    }}
    tbody tr:hover {{
        background: #EBF5FB !important;
    }}
    tbody tr.selected {{
        background: #D6EAF8 !important;
    }}
    tbody td {{
        padding: 10px 12px;
        font-size: 13px;
        color: #2C3E50;
    }}
</style>
</head>
<body>
<table>
    <thead>
        <tr>
            <td style="width: 60px; text-align: center;">№</td>
            <td>ФИО</td>
            <td style="width: 130px; text-align: center;">Дата добавления</td>
        </tr>
    </thead>
    <tbody>
        {rows_html}
    </tbody>
</table>

<script>
var bridge = null;

new QWebChannel(qt.webChannelTransport, function(channel) {{
    bridge = channel.objects.bridge;
}});

function handleClick(personId) {{
    // Убираем выделение со всех строк
    var rows = document.querySelectorAll('tbody tr');
    rows.forEach(function(r) {{ r.classList.remove('selected'); }});

    // Выделяем текущую
    var row = document.querySelector('tr[data-id="' + personId + '"]');
    if (row) row.classList.add('selected');

    if (bridge) bridge.on_row_click(personId);
}}

function handleDblClick(personId) {{
    if (bridge) bridge.on_row_double_click(personId);
}}
</script>
</body>
</html>"""

        self.web_view.setHtml(html)

    def setup_connections(self):
        """Подключение кнопок базы данных"""
        self.main.btn_refresh_db.clicked.connect(self.refresh_database)
        self.main.btn_delete_record.clicked.connect(self.delete_selected_record)
        self.main.btn_search_text.clicked.connect(self.search_in_database)
        self.main.btn_database.clicked.connect(self.refresh_database)
        self.main.btn_add_person.clicked.connect(self._open_add_person)

    def refresh_database(self):
        """Обновление таблицы"""
        try:
            self._all_people = self.db_manager.get_all_people()
            self._render_table(self._all_people)
            self.update_statistics()
            print(f"База данных обновлена: {len(self._all_people)} записей")
        except Exception as e:
            print(f"Ошибка обновления базы данных: {e}")
            QMessageBox.warning(self.main, "Ошибка", f"Не удалось загрузить базу данных: {e}")

    def _open_details_by_id(self, person_id):
        """Открытие окна деталей по ID"""
        person_data = self.db_manager.get_person_by_id(person_id)
        if person_data:
            dlg = PersonDetailsDialog(
                person_data,
                save_callback=self.save_person_data
            )
            dlg.exec()

    def _open_add_person(self):
        dlg = AddPersonDialog(
            db_manager=self.db_manager,
            parent=self.main,
            on_saved=self.refresh_database
        )
        dlg.exec()
    def save_person_data(self, updated_person):
        """Сохранение изменённых данных человека"""
        try:
            person_id = updated_person["id"]
            self.db_manager.update_person(person_id, updated_person)
            print(f"[OK] Данные пользователя {person_id} обновлены")
            self.refresh_database()
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")

    def update_statistics(self):
        """Обновление статистики базы данных"""
        try:
            stats = self.db_manager.get_statistics()
            self.main.label_total_records.setText(f"Всего записей: {stats['total_records']}")

            last_update = stats['last_update']
            if last_update != 'Never':
                try:
                    dt = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
                    formatted_date = dt.strftime("%d.%m.%Y %H:%M")
                    self.main.label_last_update.setText(f"Последнее обновление: {formatted_date}")
                except (ValueError, AttributeError) as e:
                    print(f"Ошибка форматирования даты: {e}")
                    self.main.label_last_update.setText(f"Последнее обновление: {last_update}")
            else:
                self.main.label_last_update.setText("Последнее обновление: Never")

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
            if not self.selected_person_id:
                QMessageBox.information(self.main, "Информация", "Выберите запись для удаления")
                return

            reply = QMessageBox.question(
                self.main,
                "Подтверждение удаления",
                "Вы уверены, что хотите удалить эту запись?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                success = self.db_manager.delete_person(self.selected_person_id)
                if success:
                    self.selected_person_id = None
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
            filtered = [
                p for p in all_people
                if search_text in p['full_name'].lower()
                or search_text in p.get('notes', '').lower()
            ]

            self._render_table(filtered)
            self.main.label_total_records.setText(f"Найдено записей: {len(filtered)}")

            if not filtered:
                QMessageBox.information(self.main, "Поиск", "Записи не найдены")

        except Exception as e:
            print(f"Ошибка поиска: {e}")
            QMessageBox.warning(self.main, "Ошибка", f"Ошибка при поиске: {e}")