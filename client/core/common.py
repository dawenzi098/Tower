import json

import pygame
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

    def __init__(self, w, h, default=0):
        self.w = w
        self.h = h
        self.data = []
        self.data = [[default for y in range(h)] for x in range(w)]

    def showArray2D(self):
        for y in range(self.h):
            for x in range(self.w):
                print(self.data[x][y], end=' ')
            print("")

    def __getitem__(self, item):
        return self.data[item]


class Button:
    NORMAL = 0
    MOVE = 1
    DOWN = 2

    def __init__(self, x, y, text, imgNormal, imgMove=None, imgDown=None, callBackFunc=None, font=None, rgb=(0, 0, 0)):
        """
        初始化按钮的相关参数
        :param x: 按钮在窗体上的x坐标
        :param y: 按钮在窗体上的y坐标
        :param text: 按钮显示的文本
        :param imgNormal: surface类型,按钮正常情况下显示的图片
        :param imgMove: surface类型,鼠标移动到按钮上显示的图片
        :param imgDown: surface类型,鼠标按下时显示的图片
        :param callBackFunc: 按钮弹起时的回调函数
        :param font: pygame.font.Font类型,显示的字体
        :param rgb: 元组类型,文字的颜色
        """
        # 初始化按钮相关属性
        self.imgs = []
        if not imgNormal:
            raise Exception("请设置普通状态的图片")
        self.imgs.append(imgNormal)  # 普通状态显示的图片
        self.imgs.append(imgMove)  # 被选中时显示的图片
        self.imgs.append(imgDown)  # 被按下时的图片
        for i in range(2, 0, -1):
            if not self.imgs[i]:
                self.imgs[i] = self.imgs[i - 1]

        self.callBackFunc = callBackFunc  # 触发事件
        self.status = Button.NORMAL  # 按钮当前状态
        self.x = x
        self.y = y
        self.w = imgNormal.get_width()
        self.h = imgNormal.get_height()
        self.text = text
        self.font = font
        # 文字表面
        self.textSur = self.font.render(self.text, True, rgb)

    def draw(self, destSuf):
        dx = (self.w / 2) - (self.textSur.get_width() / 2)
        dy = (self.h / 2) - (self.textSur.get_height() / 2)
        # 先画按钮背景
        if self.imgs[self.status]:
            destSuf.blit(self.imgs[self.status], [self.x, self.y])
        # 再画文字
        destSuf.blit(self.textSur, [self.x + dx, self.y + dy])

    def colli(self, x, y):
        # 碰撞检测
        if self.x < x < self.x + self.w and self.y < y < self.y + self.h:
            return True
        else:
            return False

    def getFocus(self, x, y):
        # 按钮获得焦点时
        if self.status == Button.DOWN:
            return
        if self.colli(x, y):
            self.status = Button.MOVE
        else:
            self.status = Button.NORMAL

    def mouseDown(self, x, y):
        if self.colli(x, y):
            self.status = Button.DOWN

    def mouseUp(self):
        if self.status == Button.DOWN:  # 如果按钮的当前状态是按下状态,才继续执行下面的代码
            self.status = Button.NORMAL  # 按钮弹起,所以还原成普通状态
            if self.callBackFunc:  # 调用回调函数
                return self.callBackFunc()


class TextView:
    """
    绘制文字
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if not hasattr(self, 'surface_buf'):
            setattr(self, 'surface_buf', [])  # 设置文字表面缓冲区

    def draw_text(self, dest_sur, x, y, text, font, rgb=(0, 0, 0)):
        """
        绘制文字
        """

        # 判断文字是否在缓冲区中
        surface = None
        for buf in self.surface_buf:
            if buf['text'] == text and buf['rgb'] == rgb:
                surface = buf['surface']
                # print('从缓冲区绘制')
                # print(text)
                break

        if surface is None:
            surface = font.render(text, True, rgb)
            self.surface_buf.append({'text': text, 'rgb': rgb, 'surface': surface})
            # print('第一次绘制')

        dest_sur.blit(surface, (x, y))

    def clear_buf(self):
        """
        清空缓冲区
        """
        self.surface_buf.clear()


class ScrollList:
    """
    滚动列表
    """

    def __init__(self, x, y, w, h, surface_bg, surface_item, padding=(10, 5), spacing=10, callback=None):
        """
        构造滚动列表对象
        :param x: 在窗口中的位置
        :param y: 在窗口中的位置
        :param w: 宽度
        :param h: 高度
        :param surface_bg: 列表背景图
        :param surface_item: 列表每行的背景图
        :param padding: (上下内边距，左右内边距)
        :param spacing: 行距，第一个item的底部到下一个item的头部的距离
        :param callback: item被点中后的回调函数
        """

        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.surface_bg = surface_bg
        self.surface_item = surface_item
        self.padding = padding
        self.spacing = spacing
        self.item_list = []  # item列表,格式：{"text":"6666","font":font,"data":data}，其中data是附带数据，可有可无
        self.callback = callback  # 鼠标触发的单击事件
        self.item_h = self.surface_item.get_height()
        # 缓冲区
        self.surface_buffer = None
        self.offset_y = 0  # 缓冲区偏移量
        # 当前偏移量
        self.current_offset_y = 0
        # 鼠标是否按下
        self.is_mouse_down = False
        # 鼠标按下时的坐标(相对坐标，以滚动列表左上角为原点)
        self.m_x = 0
        self.m_y = 0

    def set_buffer(self):
        """
        创建缓冲区
        """
        # 宽度
        buffer_width = self.surface_bg.get_width() - self.padding[1] * 2
        # 高度
        buffer_height = len(self.item_list) * (self.surface_item.get_height() + self.spacing)
        # 创建缓冲区
        self.surface_buffer = pygame.Surface((buffer_width, buffer_height), flags=pygame.SRCALPHA)
        pygame.Surface.convert(self.surface_buffer)
        self.surface_buffer.fill(pygame.Color(255, 255, 255, 0))

        # 画列表
        for i in range(len(self.item_list)):
            self.surface_buffer.blit(self.surface_item, (0, i * (self.item_h + self.spacing)))
            TextView().draw_text(self.surface_buffer, 15, 22 + i * (self.item_h + self.spacing),
                                 self.item_list[i]['text'],
                                 self.item_list[i]['font'], self.item_list[i]['color'])

    def mouse_move(self, x, y):
        if not self.is_mouse_down:
            return
        # 计算偏移量
        _, d_y = self.get_dxy(x, y)
        self.current_offset_y = d_y - self.m_y
        # 限制拖动范围
        if self.current_offset_y + self.offset_y >= 0:
            self.current_offset_y = 0
            self.offset_y = 0
            # self.is_mouse_down = False

        if self.current_offset_y + self.offset_y <= self.surface_bg.get_width() - self.surface_buffer.get_height():
            self.current_offset_y = 0
            self.offset_y = self.surface_bg.get_width() - self.surface_buffer.get_height()

    def mouse_down(self, x, y):
        if not self.mouse_in_panel(x, y):
            return
        self.is_mouse_down = True
        # 获取相对坐标
        self.m_x, self.m_y = self.get_dxy(x, y)

    def mouse_up(self, x, y):
        d_x, d_y = self.get_dxy(x, y)
        if d_x == self.m_x and d_y == self.m_y:
            # 单纯的点击事件，没有拖动
            try:
                if self.callback is not None:
                    index = (-self.offset_y + self.m_y) // (self.item_h + self.spacing)
                    self.callback(self.item_list[index]['data'])
            except:  # 下标越界
                pass
        else:
            # 拖动事件
            self.offset_y += self.current_offset_y
            self.current_offset_y = 0
        self.is_mouse_down = False

    def mouse_in_panel(self, x, y):
        # 计算相对坐标
        dx, dy = self.get_dxy(x, y)

        return 0 < dx < self.w and 0 < dy < self.h

    def get_dxy(self, x, y):
        # 计算相对坐标
        dx = x - self.x
        dy = y - self.y
        return dx, dy

    def add_item(self, font, text="", color=(233, 115, 115), data=None):
        """
        添加行
        :param font: 字体
        :param text: 显示的文字
        :param color: 文字颜色
        :param data: 附带数据
        """
        item = {
            "text": text,
            "font": font,
            "color": color,
            "data": data
        }
        self.item_list.append(item)
        self.set_buffer()

    def clear_item(self):
        """
        清空列表
        """
        self.item_list = []

    def draw(self, dest_suf):
        # 画背景图
        dest_suf.blit(self.surface_bg, (self.x, self.y))
        # 画item
        dest_suf.blit(self.surface_buffer, (self.x + self.padding[1], self.y + self.padding[0]),
                      (0, -(self.current_offset_y + self.offset_y), self.surface_buffer.get_width(),
                       self.surface_bg.get_height() - self.padding[0] * 2))
