import pickle
# raw dict to dict
def convertDict(rdict):
    dict = {}
    for (rk, rv) in rdict.items():
        k = str(rk, encoding = 'utf-8')
        v = pickle.loads(rv)
        dict[k] = v
    return dict

# 不处理递归
def prettyPrint(dict):
    for (k, v) in dict.items():
        # 为向量保留的开头，不打印出来
        if k[0] != '_':
            print(k)
            print(v)
            print('******')
def dictToString(dict):
    str = ''
    for (k, v) in dict.items():
        # 为向量保留的开头，不打印出来
        if k[0] != '_':
            str += k
            str += ':'
            str += v
            str += '\n'
    return str
