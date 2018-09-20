"""
登录场景的游戏逻辑
"""
import json

import pygame

from core.common import post_data
from core.game_global import Global
from core.models import Player


def start_logic():
    # 先调用一次渲染（由于后面input会阻塞线程，所以要先渲染，视图更新中也不用处理scene=0的情况了）
    g = Global()
    g.screen.blit(g.surface_pool[0], [0, 0])  # 画背景图
    pygame.display.flip()

    while True:
        cmd = input(
            """
输入1：登录游戏
输入2：注册帐号\n
            """
        )
        if cmd == '1':
            username = input("请输入帐号(1/2)：")
            password = input("请输入密码(2/2)：")
            data = {'username': username, 'password': password}
            res = post_data('/player/login/', data)
            if res.status_code == 200:
                py_obj = json.loads(res.text)
                g.auth = py_obj['token']
                # 初始化玩家属性
                g.player = Player(nickname=py_obj['player']['nickname'], hp=py_obj['player']['hp'],
                                  atk=py_obj['player']['atk'], defense=py_obj['player']['atk'],
                                  coin=py_obj['player']['coin'])
                # 进入游戏
                Global().scene = 2
                print("登录成功！")
                # Global.g().fade.reset()
                # Global.g().fade.sw = True
                break
            else:
                py_obj = json.loads(res.text)
                print('登录失败：', py_obj['msg'])

        elif cmd == '2':
            username = input("请输入帐号(1/4)：")
            password = input("请输入密码(2/4)：")
            email = input("请输入电子邮箱(3/4)：")
            nickname = input("请输入昵称(4/4)：")
            data = {
                "username": username,
                "password": password,
                "email": email,
                "nickname": nickname
            }
            res = post_data("/player/register/", data)
            if res.status_code == 200:
                print("注册成功！")
            else:
                py_obj = json.loads(res.text)
                print("注册失败：", py_obj['msg'])
