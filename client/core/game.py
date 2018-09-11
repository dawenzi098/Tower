import random
import sys
import time

import pygame

from game_global import Global


class Game:
    def __init__(self):
        g = Global()
        # 初始化pygame
        pygame.init()
        pygame.display.set_caption('魔塔Online')
        g.g_screen = pygame.display.set_mode([800, 600])
        g.g_font = pygame.font.SysFont("fangsong", 24)
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

        pass

    def update_view(self):
        """
        游戏视图更新
        """
        pass

    def handler_event(self):
        """
        事件处理
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
