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

