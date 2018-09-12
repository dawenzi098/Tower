from player.models import UserToken


def get_token_of_user(user):
    token, created = UserToken.objects.get_or_create(user=user)
    return token.key


def init_player(player):
    """
    初始化玩家属性
    """
    player.hp = 10
    player.atk = 1
    player.defense = 1
    player.coin = 10
    player.save()
