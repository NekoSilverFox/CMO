# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 16:57
# @Author  : Meng Jianing
# @FileName: buffer.py
# @Software: PyCharm
# @Versions: v0.1
# @Github  ：https://github.com/NekoSilverFox
# --------------------------------------------
from enum import Enum
from main import gl_time


class EventTypeBuffer(Enum):
    """在缓冲区的事件类型"""
    # 接受请求
    ARRIVE_REQUEST = 0

    # 请求结束
    EXIT_REQUEST = 1

    # 拒绝请求
    REFUSE_REQUEST = 2


class Buffer(EventTypeBuffer):
    # 当前缓冲区（Buffer）的数量
    __num_buffer = 0

    # Buffer 事件总量
    __event_num = 0

    # Buffer 共同日志。数据类型为List列表，每个时间为一个元组
    __all_buffer_log = []

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

        # 下一个事件发生时间
        # self.next_event_happen_time = None

        # 下一个事件发生 ID
        # self.next_event_happen_id = None

        # Buffer 日志。数据类型为List列表，每个时间为一个元组
        self.log = []

    @classmethod
    def get_num_buffer(cls):
        """获取当前 Buffer 的数量
        :return: Buffer 的数量
        """
        return cls.__num_buffer

    def insert_request_to_buffer(self, request):
        # 如果当前 Buffer 是空闲的就插入
        if self.isOccupy is False:
            self.isOccupy = True
            self.request_in_buffer = request
            event = self.__get_event(gl_time, EventTypeBuffer.ARRIVE_REQUEST, self.id, request)
            self.log.append(event)
            __allbu
        else:
            return False

    def __get_event(self, happen_time, event_type, buffer_id, request):
        """ 生成并返回缓冲区（Buffer）事件
        作为 **单个** 事件使用，比如：
            - 请求到达
            - 请求弹出
            - 请求因或缓冲区满被拒绝

        单个事件包含：
            - 事件发生时间
            - 事件类型
            - 缓冲区 ID
            - 请求源 ID
            - 请求 ID

        :param happen_time: 事件发生事件
        :param event_type: 事件类型
        :param buffer_id: Buffer ID
        :param request: 请求 ID
        :return 单个事件的字典
        """
        self.__event_num += 1

        buffer_event = {
            "Time": happen_time,
            "Event ID": self.__event_num,
            "Event type": event_type,
            "Buffer ID": buffer_id,
            "Request": request,
        }
        return buffer_event
