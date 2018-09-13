"""
地图编辑器场景逻辑
"""
import pygame
from pygame import Color

from core.game_global import Global, BasePanel
from core.models import Map

g = Global.g()
current_tile = 0  # 当前选中的瓦片（图块）
current_map = Map(3)  # 当前所编辑的地图数据


class Panel(BasePanel):
    """
    地板面板
    """

    def __init__(self, t, w, h):
        super().__init__(500, 0, w, h)
        self.focus = -1
        self.t = t  # 类型    0：地板

    def mouse_move(self, x, y):
        if not self.mouse_in_panel(x, y):
            self.focus = -1  # 鼠标不在面板范围内
            return
        dx, dy = self.get_dxy(x, y)
        self.focus = dx // 32 + dy // 32 * 4

    def mouse_down(self, x, y):
        if not self.mouse_in_panel(x, y):
            self.focus = -1  # 鼠标不在面板范围内
            return
        if self.t == 0:  # 地板面板
            global current_tile
            current_tile = self.focus + 1000

    def draw_focus(self):
        x = self.x + (self.focus % 4) * 32
        y = self.y + (self.focus // 4) * 32
        pygame.draw.rect(g.screen, Color(255, 0, 0), (x, y, 32, 32), 1)

    def draw(self):
        # 画图块
        g.screen.blit(g.surface_pool[2], (self.x, self.y))
        # 画焦点线框
        self.draw_focus()


class MapPanel(BasePanel):
    """
    地图面板
    """

    def __init__(self):
        super().__init__(0, 0, 416, 416)
        # 在地图二维数组中的索引
        self.index_x = -1
        self.index_y = -1

    def mouse_move(self, x, y):
        if not self.mouse_in_panel(x, y):
            return
        dx, dy = self.get_dxy(x, y)
        self.index_x = dx // 32
        self.index_y = dy // 32

    def mouse_down(self, x, y):
        if not self.mouse_in_panel(x, y):
            return
        # dx, dy = self.get_dxy(x, y)
        if 1000 <= current_tile < 2000:
            current_map.bottom[current_map.current_level][self.index_x][self.index_y] = current_tile

    def draw_focus(self):
        x = self.x + self.index_x * 32
        y = self.y + self.index_y * 32
        pygame.draw.rect(g.screen, Color(0, 255, 0), (x, y, 32, 32), 1)

    def draw(self):
        # 画焦点线框
        self.draw_focus()
        # 画地图
        for y in range(13):
            for x in range(13):
                tile_val = current_map.bottom[current_map.current_level][x][y]
                if 1000 <= tile_val < 2000:
                    g.screen.blit(g.surface_pool[2], (self.x + x * 32, self.y + y * 32),
                                  ((tile_val - 1000) % 4 * 32, (tile_val - 1000) // 4 * 32, 32, 32))


# 创建地板面板
floor_panel = Panel(0, 128, 64)
# 创建地图面板
map_panel = MapPanel()


def event_handler(event):
    """事件处理"""
    if event.type == pygame.MOUSEMOTION:
        x, y = pygame.mouse.get_pos()
        floor_panel.mouse_move(x, y)
        map_panel.mouse_move(x, y)
    elif event.type == pygame.MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        floor_panel.mouse_down(x, y)
        map_panel.mouse_down(x, y)


def logic():
    """
    逻辑处理
    """


def draw():
    """
    场景绘制
    """
    g.screen.fill(Color(100, 100, 100))

    # 绘制地板图块
    floor_panel.draw()
    # 绘制墙图块
    g.screen.blit(g.surface_pool[3], (500, 100))
    # 绘制宝石图块
    g.screen.blit(g.surface_pool[4], (650, 0))
    # 绘制门图块
    g.screen.blit(g.surface_pool[5], (650, 150), (0, 0, 128, 32))
    # 绘制钥匙图块
    g.screen.blit(g.surface_pool[6], (650, 200), (0, 0, 128, 32))
    # TODO:绘制怪物图块

    # 绘制地图
    map_panel.draw()
