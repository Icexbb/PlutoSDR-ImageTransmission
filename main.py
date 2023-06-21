import math
import os

from PIL import Image
from PySide6 import QtWidgets, QtGui, QtCore

from UI import Ui_MainWindow
from img_operate import read_image
from threads import TransmitThread, ReceiveThread


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.TxImagePath = None
        self.RxImagePath = os.path.join(os.getcwd(), "recv.jpg")
        self.TxDataToSend = None
        self.ButtonSendPicSelect.clicked.connect(self.TxSelectFile)
        self.ButtonSendStart.clicked.connect(self.TxStart)
        self.ButtonReceiveStart.clicked.connect(self.RxStart)

        self.TxThread: QtCore.QThread | None = None
        self.RxThread: QtCore.QThread | None = None

        self.Timer = QtCore.QTimer()
        self.Timer.start()
        self.Timer.timeout.connect(self.Update)

    def TxSelectFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            self, "打开文件", os.getcwd(),
            "图片文件(*.png *.jpg *.bmp *.jpeg);;all files(*.*)")
        if filename[0]:
            self.TxImagePath = filename[0]
            self.LESendPicPath.setText(self.TxImagePath)
            with open(self.TxImagePath, "rb") as fp:
                img = Image.open(fp)
                self.LabelSendPicSize.setText(f"{img.size[0]}x{img.size[1]}")
                pkt_size = 100 * 48 - 16 - 32
                num_frame = math.ceil(len(list(read_image(self.TxImagePath))) / pkt_size)
                self.LabelSendDataLength.setText(str(num_frame))
                self.TxDataToSend = fp.read()
                if img.size[0] > img.size[1]:
                    self.LabelSendImage.setPixmap(
                        QtGui.QPixmap(self.TxImagePath).scaledToWidth(self.LabelSendImage.width()))
                else:
                    self.LabelSendImage.setPixmap(
                        QtGui.QPixmap(self.TxImagePath).scaledToHeight(self.LabelSendImage.height()))
        else:
            self.TxImagePath = None
            self.TxDataToSend = None
            self.LabelSendImage.clear()
            self.LabelSendPicSize.clear()
            self.LabelSendDataLength.clear()
            self.LESendPicPath.clear()

    def TxStart(self):
        if self.TxImagePath:
            try:
                self.TxThread = TransmitThread(self.TxImagePath, self.LESendPlutoIP.text())
                self.TxThread.start()

            except Exception as e:
                self.TxThread = None
                raise e

    def RxStart(self):
        try:
            self.RxThread = ReceiveThread(self.RxImagePath, self.LEReceivePlutoIp.text(),
                                          self.SpinReceiveFrameCount.value())
            self.RxThread.start()
        except Exception as e:
            self.RxThread = None
            raise e

    def Update(self):
        if self.TxThread:
            if self.TxThread.isFinished():
                self.TxThread = None
                self.LabelSendImage.clear()
            elif self.TxThread.isRunning():
                self.ButtonSendStart.setDisabled(True)
            else:
                self.ButtonSendStart.setDisabled(False)
        else:
            self.ButtonSendStart.setDisabled(False)

        if self.RxThread:
            if self.RxThread.isFinished():
                self.RxThread = None
                if os.path.exists(self.RxImagePath):
                    with open(self.RxImagePath, "rb") as fp:
                        img = Image.open(fp)
                        self.LabelReceivePicSize.setText(f"{img.size[0]}x{img.size[1]}")
                        pkt_size = 100 * 48 - 16 - 32
                        num_frame = math.ceil(len(list(read_image(self.TxImagePath))) / pkt_size)
                        self.LabelReceiveDataLength.setText(str(num_frame))
                        if img.size[0] > img.size[1]:
                            self.LabelReceiveImage.setPixmap(
                                QtGui.QPixmap(self.TxImagePath).scaledToWidth(self.LabelSendImage.width()))
                        else:
                            self.LabelReceiveImage.setPixmap(
                                QtGui.QPixmap(self.TxImagePath).scaledToHeight(self.LabelSendImage.height()))
            elif self.RxThread.isRunning():
                self.ButtonReceiveStart.setDisabled(True)
            else:
                self.ButtonReceiveStart.setDisabled(False)
        else:
            self.ButtonReceiveStart.setDisabled(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    win = Window()
    win.show()
    app.exec()
