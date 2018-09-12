# Create your views here.
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from TowerServer.shortcut.response import bad_response, good_response
from TowerServer.shortcut.utils import check_str_len, check_email
from player.models import Player
from player.serializers import PlayerSrlz
from player.service import init_player, get_token_of_user


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        """
        注册账号
        """

        # 参数校验
        fields = ('username', 'password', 'email', 'nickname')
        for field in fields:
            if field not in request.data:
                return bad_response('缺少参数：' + field)

        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        nickname = request.data['nickname']

        # 账号密码长度校验
        if not check_str_len(username, 8, 16) or not check_str_len(password, 8, 16):
            return bad_response('用户名和密码长度在8~16个字符之间。')

        # 昵称长度校验
        if not check_str_len(nickname, 2, 8):
            return bad_response('昵称长度在2~8个字符之间。')

        # 邮箱校验
        if not check_email(email):
            return bad_response('电子邮箱格式错误。')

        # 逻辑校验
        if Player.objects.filter(Q(username=username) | Q(nickname=nickname)).exists():
            return bad_response('帐号或昵称已存在。')

        # 创建玩家
        player = Player(username=username, password=password, nickname=nickname, email=email)
        # 初始化玩家属性
        init_player(player)
        return good_response('注册账号成功！')


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        """
        登录
        """
        # 参数校验
        fields = ('username', 'password')
        for field in fields:
            if field not in request.data:
                return bad_response('缺少参数：' + field)

        username = request.data['username']
        password = request.data['password']
        # 验证帐号密码
        player = Player.objects.filter(username=username, password=password).first()
        if player is None:
            return bad_response('账号或密码错误！')

        token = get_token_of_user(player)
        srlz = PlayerSrlz(player)
        # 登录成功，返回token
        return Response(data={
            'token': token,
            'player': srlz.data
        })
