import pygame

from core.common import ScrollList
from core.game_global import Global


def func(data):
    print(data)


map_list = ScrollList(20, 50, 226, 404, Global().surface_pool[15], Global().surface_pool[16], padding=(10, 2),
                      callback=func)
map_list.add_item(Global().min_font, "作者", data="你好啊，这是附加数据。")
map_list.add_item(Global().min_font, "狡猾的皮球", data=[6, 6, 6])
map_list.add_item(Global().min_font, "QQ871245007", data={"attr": "name"})
map_list.add_item(Global().min_font, "发布时间")
map_list.add_item(Global().min_font, "2018年9月20日")
map_list.add_item(Global().min_font, "6666666")


def logic():
    pass


def draw():
    # 绘制界面背景
    Global().screen.blit(Global().surface_pool[14], (0, 0))
    # 绘制滚动列表
    map_list.draw(Global().screen)


def event_handler(event):
    x, y = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEMOTION:  # 鼠标移动
        map_list.mouse_move(x, y)
    elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标按下
        map_list.mouse_down(x, y)
    elif event.type == pygame.MOUSEBUTTONUP:  # 鼠标弹起
        map_list.mouse_up(x, y)


def init_scene():
    """
    初始化场景
    """
