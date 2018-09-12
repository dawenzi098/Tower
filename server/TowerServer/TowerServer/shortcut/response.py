from rest_framework import status
from rest_framework.response import Response


def bad_response(msg=None):
    """
    返回一个400的res，如果msg不为空，那么会添加一个msg字段，值为msg参数
    """
    data = {
        "msg": msg,
    }
    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


def good_response(msg=None):
    """
    返回一个200的res，如果msg不为空，那么会添加一个msg字段，值为msg参数
    """
    data = {
        "msg": msg,
    }
    return Response(data=data, status=status.HTTP_200_OK)