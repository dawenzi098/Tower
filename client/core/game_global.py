import os

import pygame


class Global:
    """
    Global的动态属性：
    screen：窗体surface
    font：游戏字体
    scene：当前场景值   0：登录或注册场景
    base_dir：项目根目录绝对路径
    surface_pool：表面池（列表），一次性加载所有图片
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance


def init_surface_pool():
    """
    按顺序加载所有图片并保存至全局变量中
    """

    g = Global()
    g.surface_pool = []

    # 0:加载登录界面图片
    g.surface_pool.append(pygame.image.load(os.path.join(g.base_dir, 'data/image/start.jpg')))
