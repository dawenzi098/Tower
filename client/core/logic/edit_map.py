"""
地图编辑器场景逻辑
"""
import pygame
from pygame import Color

from core.common import Button, TextView
from core.game_global import Global, BasePanel
from core.models import Map

g = Global()
current_tile = 0  # 当前选中的瓦片（图块）
current_map = Map(1)  # 当前所编辑的地图数据
action = None  # 动作（当进入这个场景时，可将参数传入这里）


class Panel(BasePanel):
    """
    地板面板
    """

    def __init__(self, t, x, y, w, h):
        super().__init__(x, y, w, h)
        self.focus = -1
        self.t = t  # 类型    0：地板    1：墙     2：宝石    3：门     4：钥匙    8：传送门

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

        global current_tile
        """
        1000地板 2000墙 3000宝石 4000门   5000钥匙  9000出口 9001入口
        """
        current_tile = self.focus + (self.t + 1) * 1000

    def draw_focus(self):
        x = self.x + (self.focus % 4) * 32
        y = self.y + (self.focus // 4) * 32
        if self.focus != -1:
            pygame.draw.rect(g.screen, Color(255, 0, 0), (x, y, 32, 32), 1)

    def draw(self):
        # 画图块
        g.screen.blit(g.surface_pool[self.t + 2], (self.x, self.y), (0, 0, self.w, self.h))

        # 画焦点线框
        self.draw_focus()


class MonsterPanel(BasePanel):
    """
    怪物面板
    """

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.focus = -1
        self.current_frame = 0

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
        global current_tile
        current_tile = self.focus + 6000  # 怪物id从6000开始

    def draw_focus(self):
        x = self.x + (self.focus % 4) * 32
        y = self.y + (self.focus // 4) * 32
        if self.focus != -1:
            pygame.draw.rect(g.screen, Color(255, 0, 0), (x, y, 32, 32), 1)

    def logic(self):
        # 怪物动画
        self.current_frame += 0.2
        if int(self.current_frame) >= 3:
            self.current_frame = 0

    def draw(self):
        # 画图块
        for x in range(4):
            for y in range(5):
                g.screen.blit(g.surface_pool[8], (self.x + x * 32, self.y + y * 32),
                              (x * 96 + int(self.current_frame) * 32, y * 128, 32, 32))

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
        elif 2000 <= current_tile < 7000:
            current_map.top[current_map.current_level][self.index_x][self.index_y] = current_tile

        if current_tile == 9000 or current_tile == 9001:  # 只允许有一个入口或出口
            for x in range(13):
                for y in range(13):
                    if current_map.top[current_map.current_level][x][y] == current_tile:
                        current_map.top[current_map.current_level][x][y] = 0
                        break
                else:
                    continue
                break
            current_map.top[current_map.current_level][self.index_x][self.index_y] = current_tile

    def draw_focus(self):
        x = self.x + self.index_x * 32
        y = self.y + self.index_y * 32
        pygame.draw.rect(g.screen, Color(0, 255, 0), (x, y, 32, 32), 1)

    def draw(self):
        # 画地图
        for y in range(13):
            for x in range(13):
                btm_tile_val = current_map.bottom[current_map.current_level][x][y]
                top_tile_val = current_map.top[current_map.current_level][x][y]
                if 1000 <= btm_tile_val < 2000:  # 画底层
                    g.screen.blit(g.surface_pool[2], (self.x + x * 32, self.y + y * 32),
                                  ((btm_tile_val - 1000) % 4 * 32, (btm_tile_val - 1000) // 4 * 32, 32, 32))
                if 2000 <= top_tile_val < 6000 or 9000 <= top_tile_val < 10000:  # 画墙、宝石、门、钥匙、传送门
                    g.screen.blit(g.surface_pool[top_tile_val // 1000 + 1], (self.x + x * 32, self.y + y * 32),
                                  ((top_tile_val - top_tile_val // 1000 * 1000) % 4 * 32,
                                   (top_tile_val - top_tile_val // 1000 * 1000) // 4 * 32, 32, 32))

                if 6000 <= top_tile_val < 7000:  # 怪物
                    g.screen.blit(g.surface_pool[8], (self.x + x * 32, self.y + y * 32),
                                  ((top_tile_val - 6000) % 4 * 96 + int(monster_panel.current_frame) * 32,
                                   (top_tile_val - 6000) // 4 * 128, 32, 32))
        # 画焦点线框
        self.draw_focus()


# 创建地板面板
floor_panel = Panel(0, 500, 0, 128, 64)
# 创建墙面板
wall_panel = Panel(1, 500, 100, 128, 32)
# 创建宝石面板
gem_panel = Panel(2, 650, 0, 128, 128)
# 创建门面板
door_panel = Panel(3, 650, 150, 128, 32)
# 创建钥匙面板
key_panel = Panel(4, 650, 200, 128, 32)
# 创建传送门面板
tp_panel = Panel(8, 650, 250, 64, 32)
# 创建怪物面板
monster_panel = MonsterPanel(500, 240, 128, 160)
# 创建地图面板
map_panel = MapPanel()
# 创建上一层按钮
last_btn = Button(500, 450, "上一层", g.surface_pool[11], g.surface_pool[12], g.surface_pool[13], current_map.go_last,
                  g.font)
# 创建下一层按钮
next_btn = Button(650, 450, "下一层", g.surface_pool[11], g.surface_pool[12], g.surface_pool[13], current_map.go_next,
                  g.font)

# 创建保存按钮
save_btn = Button(300, 450, "保存", g.surface_pool[11], g.surface_pool[12], g.surface_pool[13], None, g.font)


def event_handler(event):
    """事件处理"""
    x, y = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEMOTION:  # 鼠标移动
        floor_panel.mouse_move(x, y)
        wall_panel.mouse_move(x, y)
        map_panel.mouse_move(x, y)
        gem_panel.mouse_move(x, y)
        door_panel.mouse_move(x, y)
        key_panel.mouse_move(x, y)
        monster_panel.mouse_move(x, y)
        tp_panel.mouse_move(x, y)
        last_btn.getFocus(x, y)
        next_btn.getFocus(x, y)
        save_btn.getFocus(x, y)
    elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标按下
        floor_panel.mouse_down(x, y)
        wall_panel.mouse_down(x, y)
        map_panel.mouse_down(x, y)
        gem_panel.mouse_down(x, y)
        door_panel.mouse_down(x, y)
        key_panel.mouse_down(x, y)
        monster_panel.mouse_down(x, y)
        tp_panel.mouse_down(x, y)
        last_btn.mouseDown(x, y)
        next_btn.mouseDown(x, y)
        save_btn.mouseDown(x, y)
    elif event.type == pygame.MOUSEBUTTONUP:  # 鼠标弹起
        last_btn.mouseUp()
        next_btn.mouseUp()
        save_btn.mouseUp()


def logic():
    """
    逻辑处理
    """
    monster_panel.logic()


def draw():
    """
    场景绘制
    """
    g.screen.fill(Color(100, 100, 100))

    # 绘制地板面板
    floor_panel.draw()
    # 绘制墙面板
    wall_panel.draw()
    # 绘制宝石图块
    gem_panel.draw()
    # 绘制门图块
    door_panel.draw()
    # 绘制钥匙图块
    key_panel.draw()
    # 绘制怪物图块
    monster_panel.draw()
    # 绘制传送门图块
    tp_panel.draw()
    # 绘制地图
    map_panel.draw()
    # 绘制按钮
    last_btn.draw(g.screen)
    next_btn.draw(g.screen)
    save_btn.draw(g.screen)
    # 绘制当前层数
    TextView().draw_text(g.screen, 570, 520, "当前层数：%d" % (current_map.current_level + 1), g.font, (0, 255, 255))
