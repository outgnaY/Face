import redis
import requests
import json
import pickle
from configparser import ConfigParser

class DBUtil:
    def __init__(self):
        cp = ConfigParser()
        cp.read('./config.ini')
        self.gpuServer = cp.get('servers', 'gpu_server')
        self.dataEngine = cp.get('servers', 'data_engine')
        self.faceApi = cp.get('api', 'face_api')
        self.dataApi = cp.get('api', 'data_api')
        self.redisHost = cp.get('redis', 'host')
        self.redisPort = cp.get('redis', 'port')
        self.redisDb = cp.get('redis', 'db')
        self.r = redis.Redis(host=self.redisHost, port=self.redisPort, db=self.redisDb, password=None)
    def dbGetNextId(self):
        return self.r.incr('index')
    def dbClear(self):
        # 键
        rkeys = self.r.keys()
        for rkey in rkeys:
            self.r.delete(str(rkey, encoding='utf-8'))
    def dbInit(self):
        # 建立图片比对底库，并保存信息
        with open('./dat/1.jpg', 'rb') as f:
            v = []
            req = requests.post(self.gpuServer + self.faceApi, files={'img': f})
            if (len(json.loads(req.text)['features']['face_recognize_result']) > 0):
                v = json.loads(req.text)['features']['face_recognize_result'][0]
            if v != []:
                # 存储一些基本信息
                self.r.hset('1', 'name', pickle.dumps('沈耀'))
                self.r.hset('1', 'identity', pickle.dumps('teacher'))
                self.r.hset('1', 'school', pickle.dumps('SJTU'))
                self.r.hset('1', '_vector', pickle.dumps(v))
            else:
                print('Empty vector!')

        with open('./dat/2.jpg', 'rb') as f:
            v = []
            req = requests.post(self.gpuServer + self.faceApi, files={'img': f})
            if (len(json.loads(req.text)['features']['face_recognize_result']) > 0):
                v = json.loads(req.text)['features']['face_recognize_result'][0]
            if v != []:
                # 存储一些基本信息
                self.r.hset('2', 'name', pickle.dumps('尹猛'))
                self.r.hset('2', 'identity', pickle.dumps('student'))
                self.r.hset('2', 'grade', pickle.dumps('2'))
                self.r.hset('2', 'school', pickle.dumps('SJTU'))
                self.r.hset('2', '_vector', pickle.dumps(v))
            else:
                print('Empty vector!')

        with open('./dat/3.jpg', 'rb') as f:
            v = []
            req = requests.post(self.gpuServer + self.faceApi, files={'img': f})
            if (len(json.loads(req.text)['features']['face_recognize_result']) > 0):
                v = json.loads(req.text)['features']['face_recognize_result'][0]
            if v != []:
                # 存储一些基本信息
                self.r.hset('3', 'name', pickle.dumps('王重阳'))
                self.r.hset('3', 'identity', pickle.dumps('student'))
                self.r.hset('3', 'grade', pickle.dumps('2'))
                self.r.hset('3', 'school', pickle.dumps('SJTU'))
                self.r.hset('3', '_vector', pickle.dumps(v))
            else:
                print('Empty vector!')

        # 存储最大id，用于生成下一个id
        self.r.set('index', 3)




