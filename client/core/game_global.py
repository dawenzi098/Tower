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
    auth：登录认证令牌
    player：玩家对象
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    @classmethod
    def g(cls):
        return cls.__instance


def init_surface_pool():
    """
    按顺序加载所有图片并保存至全局变量中
    """

    g = Global()
    g.surface_pool = []

    # 0:加载登录界面图片
    g.surface_pool.append(pygame.image.load(os.path.join(g.base_dir, 'data/image/start.jpg')))
    # 1:加载遮罩图片
    g.surface_pool.append(pygame.image.load(os.path.join(g.base_dir, 'data/image/fade.png')).convert())
    # 2:加载地板图片
    g.surface_pool.append(pygame.image.load(os.path.join(g.base_dir, 'data/image/floor.png')).convert_alpha())
    # 3:加载墙图片
    g.surface_pool.append(pygame.image.load(os.path.join(g.base_dir, 'data/image/wall.png')).convert_alpha())
    # 4:加载宝石图片
    g.surface_pool.append(pygame.image.load(os.path.join(g.base_dir, 'data/image/gem.png')).convert_alpha())
    # 5:加载门图片
    g.surface_pool.append(pygame.image.load(os.path.join(g.base_dir, 'data/image/door.png')).convert_alpha())
    # 6:加载钥匙图片
    g.surface_pool.append(pygame.image.load(os.path.join(g.base_dir, 'data/image/key.png')).convert_alpha())
    # 7:加载主角图片
    g.surface_pool.append(pygame.image.load(os.path.join(g.base_dir, 'data/image/role.png')).convert_alpha())
    # 8:加载怪物图片
    g.surface_pool.append(pygame.image.load(os.path.join(g.base_dir, 'data/image/monster.png')).convert_alpha())
    # 9:加载攻击动画
    g.surface_pool.append(pygame.image.load(os.path.join(g.base_dir, 'data/image/ani-atk.png')).convert_alpha())
    # 10:加载传送动画
    g.surface_pool.append(pygame.image.load(os.path.join(g.base_dir, 'data/image/ani-tp.png')).convert_alpha())
    # 11:加载按钮1
    g.surface_pool.append(pygame.image.load(os.path.join(g.base_dir, 'data/image/btn-1.png')).convert_alpha())
    # 12:加载按钮2
    g.surface_pool.append(pygame.image.load(os.path.join(g.base_dir, 'data/image/btn-2.png')).convert_alpha())
    # 13:加载按钮3
    g.surface_pool.append(pygame.image.load(os.path.join(g.base_dir, 'data/image/btn-3.png')).convert_alpha())


class Fade:
    """
    淡出淡入
    """

    def __init__(self, callback=None):
        self.sw = False  # 开关，是否启动淡入淡出
        self.callback = callback  # 回调函数
        self.state = 0  # 当前状态
        self.speed = 10
        self.alpha = 0
        self.surface = Global.g().surface_pool[1]
        self.surface.set_alpha(self.alpha)

    def logic(self):
        if not self.sw:
            return

        if self.state == 0:  # 第一阶段，淡出
            self.alpha += self.speed
            if self.alpha >= 255:
                self.alpha = 255
                if self.callback:
                    self.callback()
                self.state = 1

        elif self.state == 1:  # 第二阶段，淡入
            self.alpha -= self.speed
            if self.alpha <= 0:
                self.sw = False

        self.surface.set_alpha(self.alpha)

    def draw(self):
        if not self.sw:
            return
        Global.g().screen.blit(self.surface, (0, 0))

    def reset(self, callback=None):
        self.sw = False  # 开关，是否启动淡入淡出
        self.callback = callback  # 回调函数
        self.state = 0  # 当前状态
        self.speed = 2
        self.alpha = 0
        self.surface = Global.g().surface_pool[1]
        self.surface.set_alpha(self.alpha)


class BasePanel:
    """
    基本面板
    """

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def mouse_down(self, x, y):
        pass

    def mouse_up(self, x, y):
        pass

    def mouse_move(self, x, y):
        pass

    def mouse_in_panel(self, x, y):
        # 计算相对坐标
        dx, dy = self.get_dxy(x, y)

        return 0 < dx < self.w and 0 < dy < self.h

    def get_dxy(self, x, y):
        # 计算相对坐标
        dx = x - self.x
        dy = y - self.y
        return dx, dy
