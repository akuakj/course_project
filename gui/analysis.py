# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'analysis.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGroupBox, QHBoxLayout,
    QLabel, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QTextEdit, QVBoxLayout, QWidget)

class Ui_AnalysisDialog(object):
    def setupUi(self, AnalysisDialog):
        if not AnalysisDialog.objectName():
            AnalysisDialog.setObjectName(u"AnalysisDialog")
        AnalysisDialog.resize(700, 519)
        self.verticalLayout = QVBoxLayout(AnalysisDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.label_status = QLabel(AnalysisDialog)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setStyleSheet(u"QLabel {\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    color: #2C3E50;\n"
"    padding: 10px;\n"
"    background-color: #EBF5FB;\n"
"    border-radius: 5px;\n"
"}")
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_status)

        self.progressBar = QProgressBar(AnalysisDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
"    border: 1px solid #BDC3C7;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"    height: 25px;\n"
"    font-size: 12px;\n"
"}\n"
"QProgressBar::chunk {\n"
"    background-color: #3498DB;\n"
"    border-radius: 4px;\n"
"}")
        self.progressBar.setValue(0)

        self.verticalLayout.addWidget(self.progressBar)

        self.groupBox_spectrogram = QGroupBox(AnalysisDialog)
        self.groupBox_spectrogram.setObjectName(u"groupBox_spectrogram")
        self.groupBox_spectrogram.setStyleSheet(u"QGroupBox {\n"
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
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_spectrogram)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_spectrogram = QLabel(self.groupBox_spectrogram)
        self.label_spectrogram.setObjectName(u"label_spectrogram")
        self.label_spectrogram.setMinimumSize(QSize(0, 200))
        self.label_spectrogram.setStyleSheet(u"QLabel {\n"
"    background-color: #F8F9F9;\n"
"    border: 2px dashed #BDC3C7;\n"
"    color: #7F8C8D;\n"
"    font-size: 16px;\n"
"    border-radius: 5px;\n"
"}")
        self.label_spectrogram.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_spectrogram)


        self.verticalLayout.addWidget(self.groupBox_spectrogram)

        self.groupBox_results = QGroupBox(AnalysisDialog)
        self.groupBox_results.setObjectName(u"groupBox_results")
        self.groupBox_results.setStyleSheet(u"QGroupBox {\n"
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
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_results)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.textEdit_results = QTextEdit(self.groupBox_results)
        self.textEdit_results.setObjectName(u"textEdit_results")
        self.textEdit_results.setStyleSheet(u"QTextEdit {\n"
"    border: 1px solid #BDC3C7;\n"
"    border-radius: 5px;\n"
"    padding: 10px;\n"
"    font-size: 14px;\n"
"    background-color: #F8F9F9;\n"
"}")

        self.verticalLayout_3.addWidget(self.textEdit_results)


        self.verticalLayout.addWidget(self.groupBox_results)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_save = QPushButton(AnalysisDialog)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setEnabled(False)
        self.btn_save.setStyleSheet(u"QPushButton {\n"
"    background-color: #27AE60;\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 10px 20px;\n"
"    border-radius: 5px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #229954;\n"
"}\n"
"QPushButton:disabled {\n"
"    background-color: #BDC3C7;\n"
"}")

        self.horizontalLayout.addWidget(self.btn_save)

        self.btn_close = QPushButton(AnalysisDialog)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setStyleSheet(u"QPushButton {\n"
"    background-color: #E74C3C;\n"
"    color: white;\n"
"    border: none;\n"
"    padding: 10px 20px;\n"
"    border-radius: 5px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #C0392B;\n"
"}")

        self.horizontalLayout.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(AnalysisDialog)

        QMetaObject.connectSlotsByName(AnalysisDialog)
    # setupUi

    def retranslateUi(self, AnalysisDialog):
        AnalysisDialog.setWindowTitle(QCoreApplication.translate("AnalysisDialog", u"\u0410\u043d\u0430\u043b\u0438\u0437 \u0430\u0443\u0434\u0438\u043e", None))
        self.label_status.setText(QCoreApplication.translate("AnalysisDialog", u"\u0410\u043d\u0430\u043b\u0438\u0437 \u0437\u0430\u043f\u0443\u0449\u0435\u043d... \u041f\u043e\u0434\u043e\u0436\u0434\u0438\u0442\u0435 \u043f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430", None))
        self.groupBox_spectrogram.setTitle(QCoreApplication.translate("AnalysisDialog", u"\u0421\u043f\u0435\u043a\u0442\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430", None))
        self.label_spectrogram.setText(QCoreApplication.translate("AnalysisDialog", u"\u0417\u0434\u0435\u0441\u044c \u0431\u0443\u0434\u0435\u0442 \u0441\u043f\u0435\u043a\u0442\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430 \u0438\u0437 Wolfram Mathematica", None))
        self.groupBox_results.setTitle(QCoreApplication.translate("AnalysisDialog", u"\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u0430\u043d\u0430\u043b\u0438\u0437\u0430", None))
        self.textEdit_results.setPlaceholderText(QCoreApplication.translate("AnalysisDialog", u"\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u0430\u043d\u0430\u043b\u0438\u0437\u0430 \u043f\u043e\u044f\u0432\u044f\u0442\u0441\u044f \u0437\u0434\u0435\u0441\u044c...", None))
        self.btn_save.setText(QCoreApplication.translate("AnalysisDialog", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b", None))
        self.btn_close.setText(QCoreApplication.translate("AnalysisDialog", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi

