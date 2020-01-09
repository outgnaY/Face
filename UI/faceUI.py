from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys

# 基本界面布局类
class FaceUI(object):
    def setupUi(self, Face):
        Face.setObjectName("Face")
        # 获得屏幕尺寸
        self.w = QtWidgets.QApplication.desktop().width()
        self.h = QtWidgets.QApplication.desktop().height()
        Face.resize(self.w, self.h)
        # layout
        self.layoutWidget = QtWidgets.QWidget(Face)
        # self.layoutWidget.setGeometry(QtCore.QRect(10, 150, 1.0*self.w, 0.9*self.h))
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 1.0 * self.w, 1.0 * self.h))
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setStyleSheet('background-color: rgb(43, 43, 43)')
        # startButton
        '''
        self.startButton = QtWidgets.QPushButton(Face)
        self.startButton.setGeometry(QtCore.QRect(0.1*self.w, 0.8*self.h, 93, 28))
        self.startButton.setObjectName("startButton")
        '''
        # pauseButton
        '''
        self.pauseButton = QtWidgets.QPushButton(Face)
        self.pauseButton.setGeometry(QtCore.QRect(0.8*self.w, 0.8*self.h, 93, 28))
        self.pauseButton.setObjectName("pauseButton")
        '''
        # titleLabel
        self.titleLabel = QtWidgets.QLabel(self.layoutWidget)
        self.titleLabel.setGeometry(QtCore.QRect(0, 0, self.w, 150))
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setMinimumSize(QtCore.QSize(self.w, 150))
        self.titleLabel.setText("人脸识别展示系统")
        self.titleLabel.setAlignment(Qt.Qt.AlignCenter)
        self.titleLabel.setStyleSheet("color: white")
        # font
        self.titleFont = QtGui.QFont()
        self.titleFont.setFamily("微软雅黑")
        self.titleFont.setPointSize(30)
        self.titleLabel.setFont(self.titleFont)

        # cameraLabel
        self.cameraLabel = QtWidgets.QLabel(self.layoutWidget)
        self.cameraLabel.setGeometry(QtCore.QRect(10, 150, 0.6*self.w, 0.75*self.h))
        self.cameraLabel.setMinimumSize(QtCore.QSize(0.6*self.w, 0.75*self.h))
        self.cameraLabel.setObjectName("cameraLabel")
        # font
        self.camFont = QtGui.QFont()
        self.camFont.setPointSize(14)
        self.cameraLabel.setFont(self.camFont)
        # pictureLabel
        self.picLabel = QtWidgets.QLabel(self.layoutWidget)
        self.picLabel.setGeometry(QtCore.QRect(10 + 0.62*self.w, 150, 0.35*self.w, 0.45*self.h))
        self.picLabel.setMinimumSize(QtCore.QSize(0.35*self.w, 0.45*self.h))
        self.picLabel.setObjectName("picLabel")

        # text area
        self.textLabel = QtWidgets.QLabel(self.layoutWidget)
        self.textLabel.setGeometry(QtCore.QRect(10 + 0.62 * self.w, 150 + 0.48 * self.h, 0.35 * self.w, 0.27 * self.h))
        self.textLabel.setMinimumSize(QtCore.QSize(0.35 * self.w, 0.27 * self.h))
        self.textLabel.setObjectName("textLabel")
        self.textLabel.setAlignment(Qt.Qt.AlignCenter)
        self.textLabel.setStyleSheet('border-width: 2px; border-style: solid; background-color: rgb(43, 43, 43); color: white')
        # font for text area
        self.textFont = QtGui.QFont()
        self.textFont.setFamily("微软雅黑")
        self.textFont.setPointSize(20)
        self.textLabel.setFont(self.textFont)
        # timer
        # self.timer_camera = QtCore.QTimer()
        self.retranslateUi(Face)
        QtCore.QMetaObject.connectSlotsByName(Face)

    def retranslateUi(self, Face):
        _translate = QtCore.QCoreApplication.translate
        Face.setWindowTitle(_translate("Face", "Face"))
        # self.startButton.setText(_translate("Face", "start"))
        # self.pauseButton.setText(_translate("Face", "pause"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = FaceUI()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())