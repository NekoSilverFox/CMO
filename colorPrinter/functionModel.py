# -*- coding: utf-8 -*-
# @Time    : 2021/11/24 10:34
# @Author  : Meng Jianing
# @FileName: functionModel.py
# @Software: PyCharm
# @Versions: v0.1
# @Github  ：https://github.com/NekoSilverFox
# --------------------------------------------
from colorPrinter.showType import ShowType


class ColorPrinter:
    """字符串颜色输出及显示的主功能模块"""
    @staticmethod
    def color_print(string, fore_color=None, background_color=None, show_type=ShowType.DEFAULT):
        """ 打印带有颜色及格式的字符串

        :param string: 需要输出的字符串
        :param fore_color: 字体颜色, 默认无效果
        :param background_color: 背景色, 默认无效果
        :param show_type: 显示方式, 默认无效果
        :return: 无返回值
        """
        str = ColorPrinter.get_color_string(string, fore_color, background_color, show_type)
        print(str)
        return


    @staticmethod
    def get_color_string(string, fore_color=None, background_color=None, show_type=ShowType.DEFAULT):
        """ 得到带有颜色及格式的字符串

        :param string: 需要输出的字符串
        :param fore_color: 字体颜色, 默认无效果
        :param background_color: 背景色, 默认无效果
        :param show_type: 显示方式, 默认无效果
        :return: 带有颜色及格式的字符串
        """
        # 如果全是默认值
        if fore_color is None \
                and background_color is None \
                and show_type is ShowType.DEFAULT:
            return string

        # 具有非默认值的情况，也就是有的字符串具有属性
        str = "\033["

        # 增加显示类型
        str = str + show_type

        # 增加文字颜色
        if fore_color is not None:
            str = str + ";" + fore_color

        # 增加背景色
        if background_color is not None:
            str = str + ";" + background_color

        # 拼接字符串
        str = str + "m" + string + "\033[0m"

        return str
