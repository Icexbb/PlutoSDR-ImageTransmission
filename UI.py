# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 480)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(640, 480))
        MainWindow.setMaximumSize(QSize(640, 480))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.TabTx = QWidget()
        self.TabTx.setObjectName(u"TabTx")
        self.horizontalLayout_4 = QHBoxLayout(self.TabTx)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.frame = QFrame(self.TabTx)
        self.frame.setObjectName(u"frame")
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.LabelSendImage = QLabel(self.frame)
        self.LabelSendImage.setObjectName(u"LabelSendImage")
        self.LabelSendImage.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.LabelSendImage)

        self.line = QFrame(self.frame)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.horizontalFrame = QFrame(self.frame)
        self.horizontalFrame.setObjectName(u"horizontalFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.horizontalFrame.sizePolicy().hasHeightForWidth())
        self.horizontalFrame.setSizePolicy(sizePolicy1)
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.horizontalFrame)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.LabelSendPicSize = QLabel(self.horizontalFrame)
        self.LabelSendPicSize.setObjectName(u"LabelSendPicSize")

        self.horizontalLayout_3.addWidget(self.LabelSendPicSize)

        self.label_3 = QLabel(self.horizontalFrame)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.LabelSendDataLength = QLabel(self.horizontalFrame)
        self.LabelSendDataLength.setObjectName(u"LabelSendDataLength")

        self.horizontalLayout_3.addWidget(self.LabelSendDataLength)


        self.verticalLayout_2.addWidget(self.horizontalFrame)


        self.horizontalLayout_4.addWidget(self.frame)

        self.line_4 = QFrame(self.TabTx)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_4.addWidget(self.line_4)

        self.frame1 = QFrame(self.TabTx)
        self.frame1.setObjectName(u"frame1")
        self.verticalLayout = QVBoxLayout(self.frame1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.frame1)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.LESendPlutoIP = QLineEdit(self.groupBox)
        self.LESendPlutoIP.setObjectName(u"LESendPlutoIP")

        self.horizontalLayout_2.addWidget(self.LESendPlutoIP)


        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalGroupBox = QGroupBox(self.frame1)
        self.horizontalGroupBox.setObjectName(u"horizontalGroupBox")
        self.verticalLayout_5 = QVBoxLayout(self.horizontalGroupBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(9, 9, 9, 9)
        self.LESendPicPath = QLineEdit(self.horizontalGroupBox)
        self.LESendPicPath.setObjectName(u"LESendPicPath")
        self.LESendPicPath.setReadOnly(True)

        self.verticalLayout_5.addWidget(self.LESendPicPath)

        self.ButtonSendPicSelect = QPushButton(self.horizontalGroupBox)
        self.ButtonSendPicSelect.setObjectName(u"ButtonSendPicSelect")

        self.verticalLayout_5.addWidget(self.ButtonSendPicSelect)


        self.verticalLayout.addWidget(self.horizontalGroupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.ButtonSendStart = QPushButton(self.frame1)
        self.ButtonSendStart.setObjectName(u"ButtonSendStart")

        self.verticalLayout.addWidget(self.ButtonSendStart)


        self.horizontalLayout_4.addWidget(self.frame1)

        self.horizontalLayout_4.setStretch(0, 3)
        self.horizontalLayout_4.setStretch(2, 1)
        self.tabWidget.addTab(self.TabTx, "")
        self.TabRx = QWidget()
        self.TabRx.setObjectName(u"TabRx")
        self.horizontalLayout_8 = QHBoxLayout(self.TabRx)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.frame2 = QFrame(self.TabRx)
        self.frame2.setObjectName(u"frame2")
        self.verticalLayout_4 = QVBoxLayout(self.frame2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.LabelReceiveImage = QLabel(self.frame2)
        self.LabelReceiveImage.setObjectName(u"LabelReceiveImage")
        self.LabelReceiveImage.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.LabelReceiveImage)

        self.line_2 = QFrame(self.frame2)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.horizontalFrame_2 = QFrame(self.frame2)
        self.horizontalFrame_2.setObjectName(u"horizontalFrame_2")
        sizePolicy1.setHeightForWidth(self.horizontalFrame_2.sizePolicy().hasHeightForWidth())
        self.horizontalFrame_2.setSizePolicy(sizePolicy1)
        self.horizontalLayout_7 = QHBoxLayout(self.horizontalFrame_2)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_7 = QLabel(self.horizontalFrame_2)
        self.label_7.setObjectName(u"label_7")
        sizePolicy1.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy1)

        self.horizontalLayout_7.addWidget(self.label_7)

        self.LabelReceivePicSize = QLabel(self.horizontalFrame_2)
        self.LabelReceivePicSize.setObjectName(u"LabelReceivePicSize")

        self.horizontalLayout_7.addWidget(self.LabelReceivePicSize)

        self.label_9 = QLabel(self.horizontalFrame_2)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_7.addWidget(self.label_9)

        self.LabelReceiveDataLength = QLabel(self.horizontalFrame_2)
        self.LabelReceiveDataLength.setObjectName(u"LabelReceiveDataLength")

        self.horizontalLayout_7.addWidget(self.LabelReceiveDataLength)


        self.verticalLayout_4.addWidget(self.horizontalFrame_2)


        self.horizontalLayout_8.addWidget(self.frame2)

        self.line_3 = QFrame(self.TabRx)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_8.addWidget(self.line_3)

        self.frame3 = QFrame(self.TabRx)
        self.frame3.setObjectName(u"frame3")
        self.verticalLayout_3 = QVBoxLayout(self.frame3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_2 = QGroupBox(self.frame3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.LEReceivePlutoIp = QLineEdit(self.groupBox_2)
        self.LEReceivePlutoIp.setObjectName(u"LEReceivePlutoIp")

        self.verticalLayout_6.addWidget(self.LEReceivePlutoIp)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.frame3)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.SpinReceiveFrameCount = QSpinBox(self.groupBox_3)
        self.SpinReceiveFrameCount.setObjectName(u"SpinReceiveFrameCount")

        self.verticalLayout_7.addWidget(self.SpinReceiveFrameCount)


        self.verticalLayout_3.addWidget(self.groupBox_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.ButtonReceiveStart = QPushButton(self.frame3)
        self.ButtonReceiveStart.setObjectName(u"ButtonReceiveStart")

        self.verticalLayout_3.addWidget(self.ButtonReceiveStart)


        self.horizontalLayout_8.addWidget(self.frame3)

        self.horizontalLayout_8.setStretch(0, 3)
        self.horizontalLayout_8.setStretch(2, 1)
        self.tabWidget.addTab(self.TabRx, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.LabelSendImage.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u56fe\u50cf", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u5927\u5c0f\uff1a", None))
        self.LabelSendPicSize.setText(QCoreApplication.translate("MainWindow", u"0x0", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u957f\u5ea6\uff1a", None))
        self.LabelSendDataLength.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Pluto IP", None))
        self.LESendPlutoIP.setText(QCoreApplication.translate("MainWindow", u"192.168.2.1", None))
        self.LESendPlutoIP.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Pluto IP", None))
        self.horizontalGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u56fe\u7247", None))
        self.ButtonSendPicSelect.setText(QCoreApplication.translate("MainWindow", u"\u6d4f\u89c8", None))
        self.ButtonSendStart.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u53d1\u9001", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TabTx), QCoreApplication.translate("MainWindow", u"\u53d1\u9001", None))
        self.LabelReceiveImage.setText(QCoreApplication.translate("MainWindow", u"\u7b49\u5f85\u63a5\u6536", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u5927\u5c0f\uff1a", None))
        self.LabelReceivePicSize.setText(QCoreApplication.translate("MainWindow", u"0x0", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u957f\u5ea6\uff1a", None))
        self.LabelReceiveDataLength.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Pluto IP", None))
        self.LEReceivePlutoIp.setText(QCoreApplication.translate("MainWindow", u"192.168.2.1", None))
        self.LEReceivePlutoIp.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Pluto IP", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u63a5\u6536\u5e27\u6570", None))
        self.ButtonReceiveStart.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u63a5\u6536", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TabRx), QCoreApplication.translate("MainWindow", u"\u63a5\u6536", None))
    # retranslateUi

