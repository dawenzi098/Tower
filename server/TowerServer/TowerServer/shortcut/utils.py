"""
auth:FoxyBall
date:2018年8月20日 14:08:04
"""
import re


def check_str_len(src_str, min_len, max_len):
    """
    判断字符串是否在指定长度内（包含两端点）
    满足条件返回True
    :return: Bool
    """
    return min_len <= len(src_str) <= max_len


def check_not_chinese(src_str):
    """
    判断字符串中是否没有中文（中文符号不算），不建议使用该函数
    没有中文返回True
    :param src_str: 需要判断的字符串
    :return: Bool
    """
    pattern = '[\u4e00-\u9fa5]'
    ret = re.search(pattern, src_str)
    if ret:
        return False
    else:
        return True


def check_is_english(src_str):
    """
    判断字符串是否为纯英文
    纯英文返回True
    :param src_str:
    :return: Bool
    """
    ascii_a = ord('a')
    ascii_z = ord('z')
    ascii_A = ord('A')
    ascii_Z = ord('Z')

    return all((ascii_a <= ord(c) <= ascii_z) or (ascii_A <= ord(c) <= ascii_Z) for c in src_str)


def check_str_not_char(src_str, char_list=[]):
    """
    判断字符串中，是否不含有char_list中的字符
    含有返回False
    :param src_str:
    :param char_list:
    :return: Bool
    """
    return not any(c in char_list for c in src_str)


def check_str_in_ascii(src_str):
    """
    判断字符串中的所有字符串是否都在ascii表中
    :param src_str: 源字符串
    :return: Bool
    """
    return all(ord(c) <= 127 for c in src_str)


def check_email(src_str):
    s = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    if re.match(s, src_str):
        return True
    else:
        return False


