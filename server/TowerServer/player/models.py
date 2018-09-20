import binascii
import os

from django.db import models


class UserToken(models.Model):
    """
    The custom authorization token model.
    """
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(
        'Player', related_name='auth_token',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(UserToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()


class Player(models.Model):
    username = models.CharField(max_length=32, null=False, verbose_name="账号")
    password = models.CharField(max_length=32, null=False, verbose_name="密码")
    email = models.EmailField(null=False, verbose_name="电子邮箱")

    nickname = models.CharField(max_length=16, null=False, verbose_name="昵称")
    hp = models.PositiveIntegerField(null=False, default=0, verbose_name="生命值")
    atk = models.PositiveIntegerField(null=False, default=0, verbose_name="攻击力")
    defense = models.PositiveIntegerField(null=False, default=0, verbose_name="防御力")
    coin = models.PositiveIntegerField(null=False, default=0, verbose_name="金币")

    post_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = "玩家"
        verbose_name_plural = verbose_name


class Tower(models.Model):
    player = models.ForeignKey('Player', null=False, on_delete=models.CASCADE, verbose_name='建造者')
    data = models.TextField(null=False, default="{'level':0,'bottom':None,'top':None}", verbose_name="地图数据")
    post_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.player.nickname

    class Meta:
        verbose_name = "塔"
        verbose_name_plural = verbose_name


class TowerPlayer(models.Model):
    """
    玩家在塔中的数据（存档）
    """
    player = models.ForeignKey('Player', null=False, on_delete=models.CASCADE, verbose_name='玩家')
    tower = models.ForeignKey('Tower', null=False, on_delete=models.CASCADE, verbose_name='塔')

    hp = models.PositiveIntegerField(null=False, default=0, verbose_name="生命值加成")
    atk = models.PositiveIntegerField(null=False, default=0, verbose_name="攻击力加成")
    defense = models.PositiveIntegerField(null=False, default=0, verbose_name="防御力加成")
    x = models.PositiveSmallIntegerField(null=False, default=0, verbose_name="横坐标")
    y = models.PositiveSmallIntegerField(null=False, default=0, verbose_name="纵坐标")
    level = models.PositiveSmallIntegerField(null=False, default=1, verbose_name="当前层数")

    def __str__(self):
        return self.player.nickname

    class Meta:
        verbose_name = "玩家属性"
        verbose_name_plural = verbose_name
