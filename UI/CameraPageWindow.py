from UI.faceUI import FaceUI
from Utils.computeSim import cos_sim
from PyQt5 import QtWidgets, QtCore, QtGui
import time
import sys
import cv2
import argparse
import dlib
from imutils.video import VideoStream
from imutils import face_utils
import imutils
import json
import requests
from PyQt5.QtGui import QImage, QPixmap
import pickle
import redis
from Utils.util import convertDict, prettyPrint, dictToString
from configparser import ConfigParser
from Utils.dbUtil import DBUtil


# 实现具体业务功能
class CameraPageWindow(QtWidgets.QWidget, FaceUI):
    def readConfig(self):
        cp = ConfigParser()
        cp.read('./config.ini')
        self.gpuServer = cp.get('servers', 'gpu_server')
        self.dataEngine = cp.get('servers', 'data_engine')
        self.faceApi = cp.get('api', 'face_api')
        self.dataApi = cp.get('api', 'data_api')
        self.objApi = cp.get('api', 'obj_api')
        self.redisHost = cp.get('redis', 'host')
        self.redisPort = cp.get('redis', 'port')
        self.redisDb = cp.get('redis', 'db')

    def __init__(self, parent=None):
        self.readConfig()
        self.loadToMemory()
        self.timer = time.time()
        super(CameraPageWindow, self).__init__(parent)
        self.dbUtil = DBUtil()
        self.timer_camera = QtCore.QTimer()
        # 完成一些初始化工作
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-p", "--shape-predictor", default='./dat/shape_predictor_68_face_landmarks.dat',
                             help="path to facial landmark predictor")
        self.ap.add_argument("-r", "--picamera", type=int, default=-1,
                             help="whether or not the Raspberry Pi camera should be used")
        self.args = vars(self.ap.parse_args())

        self.setupUi(self)
        # 事件绑定
        self.slotInit()
        # 人脸检测相关
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.args["shape_predictor"])
    # 将redis中的数据全部加载到内存
    def loadToMemory(self):
        self.r = redis.Redis(host = self.redisHost, port = self.redisPort, db = self.redisDb, password = None)
        # 键
        rkeys = self.r.keys()
        self.dict = {}
        for rkey in rkeys:
            key = str(rkey, encoding='utf-8')
            if key == 'index':
                continue
            rdict = self.r.hgetall(key)
            d = convertDict(rdict)
            self.dict[key] = d
            # prettyPrint(d)

    def slotInit(self):
        self.startCamera()
        # self.startButton.clicked.connect(self.startCamera)
        # self.pauseButton.clicked.connect(self.pauseCamera)
        self.timer_camera.timeout.connect(self.display)

    def startCamera(self):
        print("start")
        self.vs = VideoStream().start()
        self.timer_camera.start(30)
    '''
    def pauseCamera(self):
        print("pause")
    '''
    def display(self):
        self.frame = self.vs.read()
        show = cv2.resize(self.frame, (int(0.6*self.w), int(0.75*self.h)))
        # 灰度图
        gray = cv2.cvtColor(show, cv2.COLOR_BGR2GRAY)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        # 当前时间戳，用于存图片
        now = time.time()
        t = str(now)
        shouldUpload = now - self.timer > 1

        # 每隔至少一秒截图，并上传一张图片到比对服务器
        if shouldUpload == True:
            self.timer = now
            print("save...")
            cv2.imwrite('./store/' + t + '.jpg', show)

        rects = self.detector(gray, 0)
        detected = False

        for rect in rects:
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            if len(shape) > 0:
                detected = True
            for (x, y) in shape:
                cv2.circle(show, (x, y), 3, (0, 250, 0), -1)
        showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
        # showImage.save('./store/' + t + '.jpg', "JPG", 100)
        if shouldUpload == True and detected == True:
            # 显示识别出的图片
            pic = cv2.resize(show, (int(0.35 * self.w), int(0.45 * self.h)))
            picImage = QImage(pic.data, pic.shape[1], pic.shape[0], QImage.Format_RGB888)
            self.picLabel.setPixmap(QPixmap.fromImage(picImage))
            v1 = []
            v2 = []
            with open('./store/' + t + '.jpg', 'rb') as f:
                r1 = requests.post(self.gpuServer + self.faceApi, files={'img': f})
                if (len(json.loads(r1.text)['features']['face_recognize_result']) > 0):
                    v1 = json.loads(r1.text)['features']['face_recognize_result'][0]

            # 预定下限值，如果正在识别的人脸与库中所有人脸的余弦相似度小于这个值，则认为识别失败
            lower = 0.65
            # 最大余弦相似度
            maxSim = lower
            # 对应id
            id = ''
            print(len(self.dict))
            for (k, v) in self.dict.items():
                v2 = v['_vector']
                if v1 != [] and v2 != []:
                    # print(cos_sim(v1, v2))
                    sim = cos_sim(v1, v2)
                    if sim > maxSim:
                        maxSim = sim
                        id = k
            print(maxSim)
            # 如果最大余弦相似度大于下限值，说明已经识别出结果
            if maxSim > lower:
                print("found: " + id)
                self.textLabel.setText(dictToString(self.dict[id]))
                # 请求数据服务器，更新时间
                requests.get(self.dataEngine + self.dataApi, params = {'id': id, 'name': 'come', 'value': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))})
                # data = json.dumps({'id': id, 'name': 'come', 'value': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))})
                # requests.post(self.dataEngine + self.dataApi, data)
            else:
                # 先将数据存储在底库
                id = self.dbUtil.dbGetNextId()
                self.r.hset(id, '_vector', pickle.dumps(v1))
                # 更新内存中的数据
                self.dict[str(id)] = {'_vector': v1, 'name': 'default'}
                # 请求数据服务器，增加一条数据
                data = json.dumps({'id': id, 'name': 'new_data', 'intro': 'new_data', 'template': '4', 'attrs': {'come': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)), 'vec': v1}, 'events': []})
                requests.post(self.dataEngine + self.objApi, data)
                # print("res = " + res.text)
        self.cameraLabel.setPixmap(QPixmap.fromImage(showImage))
        cv2.waitKey(1)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = CameraPageWindow()
    ui.show()
    sys.exit(app.exec_())