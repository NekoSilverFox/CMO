# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 16:57
# @Author  : Meng Jianing
# @FileName: Buffer.py
# @Software: PyCharm
# @Versions: v0.1
# @Github  ：https://github.com/NekoSilverFox
# --------------------------------------------
from enum import Enum


class EventBuffer(Enum):
    """在缓冲区的事件类型"""
    # 接受请求
    ARRIVE_REQUEST = 0

    # 请求结束
    EXIT_REQUEST = 1

    # 拒绝请求
    REFUSE_REQUEST = 2


class Buffer:
    # 当前缓冲区（Buffer）的数量
    __num_buffer = 0

    def __init__(self):
        """ 初始化并配置变量
        """
        # 每创建一个新的 Buffer 对象的时候，将数量加一
        self.__num_buffer += 1

        # 当前 Buffer 的 ID (ID 从 1 开始计算)
        self.id = self.__num_buffer

        # Buffer 的优先级
        self.priority = self.id

        # Buffer 目前是否被占用
        self.isOccupy = False

        # 当前位于 Buffer 中的请求
        self.request_in_buffer = None

        # Buffer 日志。数据类型为List列表，每个时间为一个元组
        self.log = []



    @classmethod
    def get_num_buffer(cls):
        """获取当前 Buffer 的数量
        :return: Buffer 的数量
        """
        return cls.__num_buffer

