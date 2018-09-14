from core.common import Array2D


class Player:
    def __init__(self, nickname, hp, atk, defense, coin):
        self.nickname = nickname
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.coin = coin


class Map:
    """
    游戏地图
    地图每层为13*13
    """

    def __init__(self, level):
        self.level = level  # 一共多少层（从1开始计数）
        self.current_level = 0  # 当前层（从0开始计数）
        # 初始化所有层
        self.bottom = [Array2D(13, 13, 1000) for i in range(self.level)]  # 底层
        self.top = [Array2D(13, 13) for i in range(self.level)]  # 顶层
