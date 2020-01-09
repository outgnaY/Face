from UI.CameraPageWindow import CameraPageWindow
from UI.faceUI import FaceUI
from Utils.computeSim import cos_sim
from PyQt5 import QtWidgets
import sys
import requests
from Utils.dbUtil import DBUtil

# 预先加载数据到redis
def loadData():
    dbUtil = DBUtil()
    dbUtil.dbClear()
    dbUtil.dbInit()
def appInit():
    app = QtWidgets.QApplication(sys.argv)
    ui = CameraPageWindow()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    loadData()
    appInit()