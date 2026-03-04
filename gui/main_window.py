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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(810, 520)
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
"	border-top-right-radius: 10px;\n"
"	border-bottom-right-radius: 10px;\n"
"}\n"
"QPushButton:focus {\n"
"    outline: none;\n"
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

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_buttons.addItem(self.horizontalSpacer_4)

        self.btn_analysis_audio = QPushButton(self.layoutWidget)
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

        self.horizontalLayout_buttons.addWidget(self.btn_analysis_audio)

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

        self.stackedWidget.addWidget(self.page_analysis)
        self.page_database = QWidget()
        self.page_database.setObjectName(u"page_database")
        self.groupBox_stats = QGroupBox(self.page_database)
        self.groupBox_stats.setObjectName(u"groupBox_stats")
        self.groupBox_stats.setGeometry(QRect(10, 410, 601, 61))
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
        self.btn_load_audio.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0430\u0443\u0434\u0438\u043e", None))
        self.btn_record_audio.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0438\u0441\u0430\u0442\u044c \u0430\u0443\u0434\u0438\u043e", None))
        self.btn_analysis_audio.setText(QCoreApplication.translate("MainWindow", u"\u0410\u043d\u0430\u043b\u0438\u0437\u0438\u0440\u043e\u0432\u0430\u0442\u044c", None))
        self.groupBox_file_info.setTitle(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043e \u0444\u0430\u0439\u043b\u0435", None))
        self.label_file_name.setText(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b \u043d\u0435 \u0432\u044b\u0431\u0440\u0430\u043d", None))
        self.btn_start_audio.setText(QCoreApplication.translate("MainWindow", u"\u25b6 ", None))
        self.btn_pause_audio.setText(QCoreApplication.translate("MainWindow", u"| |", None))
        self.btn_close_audio.setText(QCoreApplication.translate("MainWindow", u"\u2715", None))
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

