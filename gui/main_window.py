# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QFrame,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(805, 467)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.menu_frame = QFrame(self.centralwidget)
        self.menu_frame.setObjectName(u"menu_frame")
        self.menu_frame.setMinimumSize(QSize(185, 0))
        self.menu_frame.setMaximumSize(QSize(185, 16777215))
        self.menu_frame.setStyleSheet(u"QFrame {\n"
"    background-color: #2C3E50;\n"
"    border: none;\n"
"    border-right: 1px solid #34495E;\n"
"}")
        self.menu_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.menu_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.menu_frame)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.label = QLabel(self.menu_frame)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"QLabel {\n"
"    color: #ECF0F1;\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    padding: 10px;\n"
"    border-bottom: 1px solid #34495E;\n"
"}")

        self.verticalLayout.addWidget(self.label)

        self.btn_home = QPushButton(self.menu_frame)
        self.btn_home.setObjectName(u"btn_home")
        self.btn_home.setStyleSheet(u"QPushButton {\n"
"                background-color: #3498DB;\n"
"                color: white;\n"
"                border: none;\n"
"                padding: 12px;\n"
"                text-align: center;\n"
"                font-weight: bold;\n"
"                font-size: 14px;\n"
"                border-radius: 5px;  }\n"
"QPushButton:hover {\n"
"                background-color: #2980B9;\n"
"                padding-left: 15px;\n"
"            }")

        self.verticalLayout.addWidget(self.btn_home)

        self.btn_analyze = QPushButton(self.menu_frame)
        self.btn_analyze.setObjectName(u"btn_analyze")
        self.btn_analyze.setStyleSheet(u"QPushButton {\n"
"                background-color: #9B59B6;\n"
"                color: white;\n"
"                border: none;\n"
"                padding: 12px;\n"
"                text-align: center;\n"
"                font-weight: bold;\n"
"                font-size: 14px;\n"
"                border-radius: 5px;\n"
"            }\n"
"QPushButton:hover {\n"
"                background-color: #8E44AD;\n"
"                padding-left: 15px; }")

        self.verticalLayout.addWidget(self.btn_analyze)

        self.btn_database = QPushButton(self.menu_frame)
        self.btn_database.setObjectName(u"btn_database")
        self.btn_database.setStyleSheet(u"QPushButton {\n"
"    background-color: #E74C3C;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"    padding: 12px;\n"
"    text-align: center;\n"
"    font-size: 14px;\n"
"    border-radius: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #C0392B;\n"
"    padding-left: 15px;\n"
"}")

        self.verticalLayout.addWidget(self.btn_database)

        self.btn_ai = QPushButton(self.menu_frame)
        self.btn_ai.setObjectName(u"btn_ai")
        self.btn_ai.setStyleSheet(u"QPushButton {\n"
"    background-color: #2ECC71;\n"
"    color: white;\n"
"	font-weight: bold;\n"
"    border: none;\n"
"    padding: 12px;\n"
"    text-align: center;\n"
"    font-size: 14px;\n"
"    border-radius: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #27AE60;\n"
"    padding-left: 15px;\n"
"}")

        self.verticalLayout.addWidget(self.btn_ai)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.menu_frame)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background-color: rgba(240, 248, 255, 1);\n"
"\n"
"")
        self.page_start = QWidget()
        self.page_start.setObjectName(u"page_start")
        self.verticalLayoutWidget = QWidget(self.page_start)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 591, 391))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"font-size: 24px; font-weight: bold; color: #2C3E50; padding: 10px;\n"
"\n"
"")

        self.verticalLayout_4.addWidget(self.label_3)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"font-size: 14px; color: #34495E; padding: 10px; font-weight: bold;\n"
"\n"
"")

        self.verticalLayout_4.addWidget(self.label_2)

        self.layoutWidget_4 = QWidget(self.page_start)
        self.layoutWidget_4.setObjectName(u"layoutWidget_4")
        self.layoutWidget_4.setGeometry(QRect(10, 420, 601, 41))
        self.horizontalLayout_buttons_4 = QHBoxLayout(self.layoutWidget_4)
        self.horizontalLayout_buttons_4.setObjectName(u"horizontalLayout_buttons_4")
        self.horizontalLayout_buttons_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_buttons_4.addItem(self.horizontalSpacer_8)

        self.btn_start = QPushButton(self.layoutWidget_4)
        self.btn_start.setObjectName(u"btn_start")
        self.btn_start.setStyleSheet(u"QPushButton {\n"
"    background-color: #3498DB;\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 8px 12px;\n"
"    border-radius: 4px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"                background-color: #2980B9;\n"
"                padding-left: 14px;\n"
"            }\n"
"")

        self.horizontalLayout_buttons_4.addWidget(self.btn_start)

        self.stackedWidget.addWidget(self.page_start)
        self.page_analysis = QWidget()
        self.page_analysis.setObjectName(u"page_analysis")
        self.layoutWidget = QWidget(self.page_analysis)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 601, 42))
        self.horizontalLayout_buttons = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_buttons.setObjectName(u"horizontalLayout_buttons")
        self.horizontalLayout_buttons.setContentsMargins(0, 0, 0, 0)
        self.btn_load_audio = QPushButton(self.layoutWidget)
        self.btn_load_audio.setObjectName(u"btn_load_audio")
        self.btn_load_audio.setStyleSheet(u"QPushButton {\n"
"    background-color: #3498DB;\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 8px 12px;\n"
"    border-radius: 4px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"                background-color: #2980B9;\n"
"                padding-left: 14px;\n"
"            }\n"
"")

        self.horizontalLayout_buttons.addWidget(self.btn_load_audio)

        self.btn_record_audio = QPushButton(self.layoutWidget)
        self.btn_record_audio.setObjectName(u"btn_record_audio")
        self.btn_record_audio.setStyleSheet(u"QPushButton {\n"
"    background-color: #3498DB;\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 8px 12px;\n"
"    border-radius: 4px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"                background-color: #2980B9;\n"
"                padding-left: 14px;\n"
"            }\n"
"")

        self.horizontalLayout_buttons.addWidget(self.btn_record_audio)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_buttons.addItem(self.horizontalSpacer)

        self.groupBox_file_info = QGroupBox(self.page_analysis)
        self.groupBox_file_info.setObjectName(u"groupBox_file_info")
        self.groupBox_file_info.setGeometry(QRect(10, 60, 601, 161))
        self.groupBox_file_info.setStyleSheet(u"QGroupBox {\n"
"    font-weight: bold;\n"
"    border: 1px solid #BDC3C7;\n"
"    border-radius: 5px;\n"
"    margin-top: 10px;\n"
"    padding-top: 10px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 5px 0 5px;\n"
"    color: #2C3E50;\n"
"}")
        self.verticalLayout_group = QVBoxLayout(self.groupBox_file_info)
        self.verticalLayout_group.setSpacing(10)
        self.verticalLayout_group.setObjectName(u"verticalLayout_group")
        self.verticalLayout_group.setContentsMargins(10, 20, 10, 10)
        self.label_file_name = QLabel(self.groupBox_file_info)
        self.label_file_name.setObjectName(u"label_file_name")
        self.label_file_name.setStyleSheet(u"QLabel {\n"
"    font-size: 14px;\n"
"    color: #7F8C8D;\n"
"    padding: 5px;\n"
"    background-color: #F8F9F9;\n"
"    border: 1px solid #EBEDEF;\n"
"    border-radius: 3px;\n"
"}")
        self.label_file_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_group.addWidget(self.label_file_name)

        self.progress_audio = QProgressBar(self.groupBox_file_info)
        self.progress_audio.setObjectName(u"progress_audio")
        self.progress_audio.setStyleSheet(u"QProgressBar {\n"
"    border: 1px solid #BDC3C7;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: #3498DB;\n"
"    border-radius: 4px;\n"
"}")
        self.progress_audio.setValue(0)

        self.verticalLayout_group.addWidget(self.progress_audio)

        self.horizontalLayout_control = QHBoxLayout()
        self.horizontalLayout_control.setObjectName(u"horizontalLayout_control")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_control.addItem(self.horizontalSpacer_5)

        self.btn_start_audio = QPushButton(self.groupBox_file_info)
        self.btn_start_audio.setObjectName(u"btn_start_audio")
        self.btn_start_audio.setEnabled(False)
        self.btn_start_audio.setStyleSheet(u"QPushButton {\n"
"    background-color: #3498DB;\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 8px 15px;\n"
"    font-size: 16px;\n"
"    border-radius: 4px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #2980B9;\n"
"}\n"
"QPushButton:disabled {\n"
"    background-color: #BDC3C7;\n"
"}")

        self.horizontalLayout_control.addWidget(self.btn_start_audio)

        self.btn_pause_audio = QPushButton(self.groupBox_file_info)
        self.btn_pause_audio.setObjectName(u"btn_pause_audio")
        self.btn_pause_audio.setEnabled(False)
        self.btn_pause_audio.setStyleSheet(u"QPushButton {\n"
"    background-color: #3498DB;\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 8px 15px;\n"
"    font-size: 15px;\n"
"    border-radius: 4px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #2980B9;\n"
"}\n"
"QPushButton:disabled {\n"
"    background-color: #BDC3C7;\n"
"}")

        self.horizontalLayout_control.addWidget(self.btn_pause_audio)

        self.btn_close_audio = QPushButton(self.groupBox_file_info)
        self.btn_close_audio.setObjectName(u"btn_close_audio")
        self.btn_close_audio.setEnabled(False)
        self.btn_close_audio.setStyleSheet(u"QPushButton {\n"
"    background-color: #3498DB;\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 8px 15px;\n"
"    font-size: 15px;\n"
"    border-radius: 4px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #2980B9;\n"
"}\n"
"QPushButton:disabled {\n"
"    background-color: #BDC3C7;\n"
"}")

        self.horizontalLayout_control.addWidget(self.btn_close_audio)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_control.addItem(self.horizontalSpacer_2)


        self.verticalLayout_group.addLayout(self.horizontalLayout_control)

        self.layoutWidget_2 = QWidget(self.page_analysis)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(10, 420, 601, 45))
        self.horizontalLayout_buttons_3 = QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_buttons_3.setObjectName(u"horizontalLayout_buttons_3")
        self.horizontalLayout_buttons_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_buttons_3.addItem(self.horizontalSpacer_6)

        self.btn_analysis_audio = QPushButton(self.layoutWidget_2)
        self.btn_analysis_audio.setObjectName(u"btn_analysis_audio")
        self.btn_analysis_audio.setStyleSheet(u"QPushButton {\n"
"    background-color: #3498DB;\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 8px 12px;\n"
"    border-radius: 4px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"                background-color: #2980B9;\n"
"                padding-left: 14px;\n"
"            }\n"
"")

        self.horizontalLayout_buttons_3.addWidget(self.btn_analysis_audio)

        self.stackedWidget.addWidget(self.page_analysis)
        self.page_database = QWidget()
        self.page_database.setObjectName(u"page_database")
        self.table_voices = QTableWidget(self.page_database)
        if (self.table_voices.columnCount() < 4):
            self.table_voices.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_voices.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_voices.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_voices.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_voices.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.table_voices.setObjectName(u"table_voices")
        self.table_voices.setGeometry(QRect(10, 140, 601, 251))
        self.table_voices.setStyleSheet(u"QTableWidget {\n"
"    border: 1px solid #BDC3C7;\n"
"    border-radius: 5px;\n"
"    background-color: white;\n"
"    alternate-background-color: #F8F9F9;\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: #34495E;\n"
"    color: white;\n"
"    padding: 8px;\n"
"    border: none;\n"
"    font-weight: bold;\n"
"}")
        self.table_voices.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self.table_voices.setAlternatingRowColors(True)
        self.table_voices.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_voices.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_voices.horizontalHeader().setMinimumSectionSize(50)
        self.table_voices.horizontalHeader().setHighlightSections(False)
        self.table_voices.horizontalHeader().setStretchLastSection(True)
        self.groupBox_stats = QGroupBox(self.page_database)
        self.groupBox_stats.setObjectName(u"groupBox_stats")
        self.groupBox_stats.setGeometry(QRect(10, 400, 601, 61))
        self.groupBox_stats.setStyleSheet(u"QGroupBox {\n"
"    font-weight: bold;\n"
"    border: 1px solid #BDC3C7;\n"
"    border-radius: 5px;\n"
"    margin-top: 10px;\n"
"    padding-top: 10px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 5px 0 5px;\n"
"    color: #2C3E50;\n"
"}")
        self.horizontalLayout_stats = QHBoxLayout(self.groupBox_stats)
        self.horizontalLayout_stats.setObjectName(u"horizontalLayout_stats")
        self.label_total_records = QLabel(self.groupBox_stats)
        self.label_total_records.setObjectName(u"label_total_records")
        self.label_total_records.setStyleSheet(u"QLabel {\n"
"    color: #2C3E50;\n"
"    font-size: 13px;\n"
"    padding: 5px;\n"
"}")

        self.horizontalLayout_stats.addWidget(self.label_total_records)

        self.label_last_update = QLabel(self.groupBox_stats)
        self.label_last_update.setObjectName(u"label_last_update")
        self.label_last_update.setStyleSheet(u"QLabel {\n"
"    color: #2C3E50;\n"
"    font-size: 13px;\n"
"    padding: 5px;\n"
"}")

        self.horizontalLayout_stats.addWidget(self.label_last_update)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_stats.addItem(self.horizontalSpacer_7)

        self.groupBox_search = QGroupBox(self.page_database)
        self.groupBox_search.setObjectName(u"groupBox_search")
        self.groupBox_search.setGeometry(QRect(10, 50, 601, 81))
        self.groupBox_search.setStyleSheet(u"QGroupBox {\n"
"    font-weight: bold;\n"
"    border: 1px solid #BDC3C7;\n"
"    border-radius: 5px;\n"
"    margin-top: 10px;\n"
"    padding-top: 10px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 5px 0 5px;\n"
"    color: #2C3E50;\n"
"}")
        self.horizontalLayout_search = QHBoxLayout(self.groupBox_search)
        self.horizontalLayout_search.setObjectName(u"horizontalLayout_search")
        self.lineEdit_search = QLineEdit(self.groupBox_search)
        self.lineEdit_search.setObjectName(u"lineEdit_search")
        self.lineEdit_search.setStyleSheet(u"QLineEdit {\n"
"    border: 1px solid #BDC3C7;\n"
"    border-radius: 4px;\n"
"    padding: 8px;\n"
"    font-size: 14px;\n"
"}\n"
"QLineEdit:focus {\n"
"    border-color: #3498DB;\n"
"}")

        self.horizontalLayout_search.addWidget(self.lineEdit_search)

        self.btn_search_text = QPushButton(self.groupBox_search)
        self.btn_search_text.setObjectName(u"btn_search_text")
        self.btn_search_text.setStyleSheet(u"QPushButton {\n"
"    background-color: #3498DB;\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 8px 15px;\n"
"    border-radius: 4px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #2980B9;\n"
"}")

        self.horizontalLayout_search.addWidget(self.btn_search_text)

        self.layoutWidget_3 = QWidget(self.page_database)
        self.layoutWidget_3.setObjectName(u"layoutWidget_3")
        self.layoutWidget_3.setGeometry(QRect(10, 10, 601, 41))
        self.horizontalLayout_control_2 = QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_control_2.setObjectName(u"horizontalLayout_control_2")
        self.horizontalLayout_control_2.setContentsMargins(0, 0, 0, 0)
        self.btn_refresh_db = QPushButton(self.layoutWidget_3)
        self.btn_refresh_db.setObjectName(u"btn_refresh_db")
        self.btn_refresh_db.setStyleSheet(u"QPushButton {\n"
"    background-color: #2ECC71;\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 8px 15px;\n"
"    border-radius: 4px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #27AE60;\n"
"}")

        self.horizontalLayout_control_2.addWidget(self.btn_refresh_db)

        self.btn_delete_record = QPushButton(self.layoutWidget_3)
        self.btn_delete_record.setObjectName(u"btn_delete_record")
        self.btn_delete_record.setStyleSheet(u"QPushButton {\n"
"    background-color: #E74C3C;\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 8px 15px;\n"
"    border-radius: 4px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #C0392B;\n"
"}")

        self.horizontalLayout_control_2.addWidget(self.btn_delete_record)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_control_2.addItem(self.horizontalSpacer_3)

        self.label_db_status = QLabel(self.layoutWidget_3)
        self.label_db_status.setObjectName(u"label_db_status")
        self.label_db_status.setStyleSheet(u"QLabel {\n"
"    color: #27AE60;\n"
"    font-weight: bold;\n"
"    padding: 5px 10px;\n"
"    background-color: #EAFAEE;\n"
"    border: 1px solid #27AE60;\n"
"    border-radius: 3px;\n"
"}")

        self.horizontalLayout_control_2.addWidget(self.label_db_status)

        self.stackedWidget.addWidget(self.page_database)
        self.page_ai = QWidget()
        self.page_ai.setObjectName(u"page_ai")
        self.stackedWidget.addWidget(self.page_ai)

        self.horizontalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"VoiceMaxxing", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0435\u043d\u044e", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0447\u0430\u043b\u043e", None))
        self.btn_analyze.setText(QCoreApplication.translate("MainWindow", u"\u0410\u043d\u0430\u043b\u0438\u0437\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435", None))
        self.btn_database.setText(QCoreApplication.translate("MainWindow", u"\u0411\u0430\u0437\u0430 \u0414\u0430\u043d\u043d\u044b\u0445", None))
        self.btn_ai.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0435\u0439\u0440\u043e\u0441\u0435\u0442\u044c", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0440\u043e \u043f\u043e\u0436\u0430\u043b\u043e\u0432\u0430\u0442\u044c!", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt;\">\u0414\u0430\u043d\u043d\u043e\u0435 \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0435 \u043f\u0440\u0435\u0434\u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u043e \u0434\u043b\u044f \u0430\u043d\u0430\u043b\u0438\u0437\u0430 \u0438 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0438 \u0433\u043e\u043b\u043e\u0441\u043e\u0432\u044b\u0445<br/>\u0434\u0430\u043d\u043d\u044b\u0445 \u0441 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u0435\u043c \u0441\u043e\u0432\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0445 \u0430\u043b\u0433\u043e\u0440\u0438\u0442\u043c\u043e\u0432 <br/>\u043c\u0430\u0448\u0438\u043d\u043d\u043e\u0433\u043e \u043e\u0431\u0443\u0447\u0435\u043d\u0438\u044f.</span></p><p><span style=\" font-size:11pt;\">\u26a0\ufe0f \u0412\u0430\u0436\u043d\u043e\u0435 \u0437\u0430\u043c\u0435\u0447\u0430\u043d\u0438\u0435:<br/>\u0414\u0430\u043d\u043d\u0430\u044f \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430"
                        " \u044f\u0432\u043b\u044f\u0435\u0442\u0441\u044f \u043b\u044e\u0431\u0438\u0442\u0435\u043b\u044c\u0441\u043a\u043e\u0439 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u043e\u0439 \u0438 \u043d\u0435 \u0434\u0430\u0451\u0442 100% <br/>\u0433\u0430\u0440\u0430\u043d\u0442\u0438\u044e \u043d\u0430 \u0430\u0431\u0441\u043e\u043b\u044e\u0442\u043d\u0443\u044e \u0442\u043e\u0447\u043d\u043e\u0441\u0442\u044c \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u043e\u0432. <br/><br/>\u042d\u0444\u0444\u0435\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u044c \u0440\u0430\u0441\u043f\u043e\u0437\u043d\u0430\u0432\u0430\u043d\u0438\u044f \u043c\u043e\u0436\u0435\u0442 \u0432\u0430\u0440\u044c\u0438\u0440\u043e\u0432\u0430\u0442\u044c\u0441\u044f \u0432 \u0437\u0430\u0432\u0438\u0441\u0438\u043c\u043e\u0441\u0442\u0438 \u043e\u0442:<br/>\u2022 \u041a\u0430\u0447\u0435\u0441\u0442\u0432\u0430 \u0432\u0445\u043e\u0434\u043d\u043e\u0433\u043e \u0430\u0443\u0434\u0438\u043e\u0441\u0438\u0433\u043d\u0430\u043b"
                        "\u0430<br/>\u2022 \u0427\u0438\u0441\u0442\u043e\u0442\u044b \u0440\u0435\u0447\u0438 \u0438 \u0434\u0438\u043a\u0446\u0438\u0438<br/>\u2022 \u0424\u043e\u043d\u043e\u0432\u044b\u0445 \u0448\u0443\u043c\u043e\u0432 \u0438 \u043f\u043e\u043c\u0435\u0445<br/>\u2022 \u042f\u0437\u044b\u043a\u043e\u0432\u044b\u0445 \u043e\u0441\u043e\u0431\u0435\u043d\u043d\u043e\u0441\u0442\u0435\u0439</span></p><p><br/></p></body></html>", None))
        self.btn_start.setText(QCoreApplication.translate("MainWindow", u"            \u27f6          ", None))
        self.btn_load_audio.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0430\u0443\u0434\u0438\u043e", None))
        self.btn_record_audio.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0438\u0441\u0430\u0442\u044c \u0430\u0443\u0434\u0438\u043e", None))
        self.groupBox_file_info.setTitle(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043e \u0444\u0430\u0439\u043b\u0435", None))
        self.label_file_name.setText(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b \u043d\u0435 \u0432\u044b\u0431\u0440\u0430\u043d", None))
        self.btn_start_audio.setText(QCoreApplication.translate("MainWindow", u"\u25b6 ", None))
        self.btn_pause_audio.setText(QCoreApplication.translate("MainWindow", u"| |", None))
        self.btn_close_audio.setText(QCoreApplication.translate("MainWindow", u"\u2715", None))
        self.btn_analysis_audio.setText(QCoreApplication.translate("MainWindow", u"\u0410\u043d\u0430\u043b\u0438\u0437\u0438\u0440\u043e\u0432\u0430\u0442\u044c", None))
        ___qtablewidgetitem = self.table_voices.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"ID", None));
        ___qtablewidgetitem1 = self.table_voices.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u0424\u0418\u041e", None));
        ___qtablewidgetitem2 = self.table_voices.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0430\u0442\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f", None));
        ___qtablewidgetitem3 = self.table_voices.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u0411\u0438\u043e. \u0434\u0430\u043d\u043d\u044b\u0435", None));
        self.groupBox_stats.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430 \u0431\u0430\u0437\u044b", None))
        self.label_total_records.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0441\u0435\u0433\u043e \u0437\u0430\u043f\u0438\u0441\u0435\u0439: 0", None))
        self.label_last_update.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0435 \u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435: -", None))
        self.groupBox_search.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0438\u0441\u043a \u043f\u043e \u0431\u0430\u0437\u0435", None))
        self.lineEdit_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0438\u043c\u044f \u0434\u043b\u044f \u043f\u043e\u0438\u0441\u043a\u0430...", None))
        self.btn_search_text.setText(QCoreApplication.translate("MainWindow", u" \u041d\u0430\u0439\u0442\u0438", None))
        self.btn_refresh_db.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c \u0411\u0414", None))
        self.btn_delete_record.setText(QCoreApplication.translate("MainWindow", u" \u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u044c", None))
        self.label_db_status.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0442\u0443\u0441 \u0411\u0414: OK", None))
    # retranslateUi

