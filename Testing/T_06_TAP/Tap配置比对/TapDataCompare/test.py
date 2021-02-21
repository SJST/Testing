# -*- coding: utf-8 -*-

# @Project  : TapDataCompare
# @File     : test.py
# @Date     : 2021-01-28
# @Author   : Administrator
# @Info     :
# @Introduce:


def update_dict(dict1, dict2, *args):
    """
        根据 arg中传入的 字段 将 dict中该字段的添加到 dict1 中 arg 是dict格式 key为dict2 中key value 为添加到dict1中所
        使用key 返回值为 dict1
    :param dict1: 目标dict
    :param dict2: 源 dict
    :param args: 字段
    :return: 目标dict
    """
    field_list = args[0]
    for key in dict2:
        if args and key in field_list.keys():
            dict1[field_list[key]] = dict2[key]
    return dict1

def tuple_list(dict1):
    value = dict1.values()
    print(value)

if __name__ == '__main__':
    a = {'名字': '张三'}
    b = {'age': '21'}
    c = {'名字': 'name'}
    d = update_dict(b, a, c)
    tuple_list(d)
