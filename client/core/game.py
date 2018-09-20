import os
import random
import sys
import time

import pygame

from core.logic.start import start_logic
from .game_global import Global, init_surface_pool, Fade


class Game:
    def __init__(self):
        g = Global()

        # 初始化pygame
        pygame.init()
        pygame.display.set_caption('魔塔Online')

        # 初始化全局变量
        g.screen = pygame.display.set_mode([800, 600])
        g.scene = 2  # TODO:发布的时候记得改
        g.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # g.font = pygame.font.SysFont('fangsong', 24)
        g.font = pygame.font.Font(os.path.join(g.base_dir, 'data/font/mh.ttf'), 24)
        g.min_font = pygame.font.Font(os.path.join(g.base_dir, 'data/font/mh.ttf'), 18)
        g.min_font.set_bold(True)
        g.host = 'http://127.0.0.1:8000'
        g.auth = '666666'
        init_surface_pool()  # 加载全部图片（一共也没几张图，占不了多少内存）
        g.fade = Fade()
        # 初始化随机种子
        random.seed(int(time.time()))

        # 进入游戏主循环
        self.main_loop()

    def main_loop(self):
        """
        游戏主循环
        """
        while True:
            # FPS=60
            pygame.time.delay(16)
            # 逻辑更新
            self.update_logic()
            # 视图更新
            self.update_view()

    def update_logic(self):
        """
        游戏逻辑更新
        """

        # 事件处理
        self.handler_event()

        Global().fade.logic()  # 淡入淡出
        # 场景逻辑
        if Global().scene == 0:  # 登录场景
            start_logic()
        elif Global().scene == 1:  # 地图编辑器
            from core.logic import edit_map
            edit_map.logic()
        elif Global().scene == 2:  # 游戏大厅
            from core.logic import game_room
            game_room.logic()

    def update_view(self):
        """
        游戏视图更新
        """

        if Global().scene == 1:
            from core.logic import edit_map
            edit_map.draw()
        elif Global().scene == 2:
            from core.logic import game_room
            game_room.draw()

        Global().fade.draw()  # 淡入淡出

        pygame.display.flip()

    def handler_event(self):
        """
        事件处理
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # 事件分发
            if Global().scene == 1:
                from core.logic import edit_map
                edit_map.event_handler(event)
            elif Global().scene == 2:
                from core.logic import game_room
                game_room.event_handler(event)
            elif Global().scene == 3:
                pass