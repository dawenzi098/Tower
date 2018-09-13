import json
import requests

from core.game_global import Global


def get_data(url):
    """
    发送数据包给服务器
    """
    g = Global()
    return requests.get(g.host + url, headers={'Authorization': g.auth})


def post_data(url, dict_data):
    """
    发送数据包给服务器
    """
    g = Global()
    j_str = json.dumps(dict_data)
    return requests.post(g.host + url, data=j_str,
                         headers={'Authorization': g.auth, 'content-type': 'application/json'})


class Array2D:
    """
        说明：
            1.构造方法需要两个参数，即二维数组的宽和高
            2.成员变量w和h是二维数组的宽和高
            3.使用：‘对象[x][y]’可以直接取到相应的值
            4.数组的默认值都是0
    """

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.data = []
        self.data = [[0 for y in range(h)] for x in range(w)]

    def showArray2D(self):
        for y in range(self.h):
            for x in range(self.w):
                print(self.data[x][y], end=' ')
            print("")

    def __getitem__(self, item):
        return self.data[item]
