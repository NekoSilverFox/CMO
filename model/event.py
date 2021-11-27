# -*- coding: utf-8 -*-
# @Time    : 2021/11/25 15:37
# @Author  : Meng Jianing
# @FileName: event.py
# @Software: PyCharm
# @Versions: v0.1
# @Github  ：https://github.com/NekoSilverFox
# --------------------------------------------

class Event:
    """记录时间，作为时间线（程序）的最小单位

    **属性：**
     - 当前时间
     - 事件类型
        - 生成请求
        - 请求进入缓冲区
        - 请求离开缓冲区
        - 请求进入处理机
        - 请求离开处理机
        - 请求被取消
     - 本 CMO 生成的第几个请求
     - 生成这个请求的源ID
     - 请求在他的生成源的ID
     - 缓冲区ID
     - 处理机ID
    """

    # 事件类型
    REQUEST_CREATE = '\033[1;32mcreate\033[0m'  # 请求被创建
    REQUEST_PUSH_IN_BUFFER = '\033[1;33mjoin buffer\033[0m'  # 请求进入缓冲区
    REQUEST_POP_FROM_BUFFER = '\033[1;33mexit buffer\033[0m'  # 请求离开缓冲区
    REQUEST_PUSH_IN_DEVICE = '\033[1;34mjoin device\033[0m'  # 请求进入处理机
    REQUEST_POP_FROM_DEVICE = '\033[1;34mexit device\033[0m'  # 请求离开处理机
    REQUEST_CANCEL = '\033[1;31mcancel\033[0m'  # 请求被取消

    def __init__(self, happen_time=None, event_type=None, request_id_in_cmo=None, source_id=None,
                 request_id_in_source=None, buffer_id=None, device_id=None):
        """创建一个请求事件

        :param happen_time: *发生时间
        :param event_type: *事件类型（使用本类名 `Event.REQUEST_????` 获得）
        :param request_id_in_cmo: *该请求在整个 CMO 系统中的 ID
        :param source_id: *产生这个请求的源的 ID
        :param request_id_in_source: *这个请求在产生它的源中的 ID
        :param buffer_id: 缓冲区 ID
        :param device_id: 处理机 ID
        """
        self.happen_time = happen_time
        self.event_type = event_type
        self.request_id_in_cmo = request_id_in_cmo
        self.source_id = source_id
        self.request_id_in_source = request_id_in_source
        self.buffer_id = buffer_id
        self.device_id = device_id

    def __str__(self):
        """ 返回事件信息的字符串

        :return: 事件信息
        """
        return format('\033[33;1m[Event]\033[0m Time: %s' % self.happen_time, "<40") \
               + format('Type: %s' % self.event_type, "<35") \
               + format('Request ID in CMO: %s' % self.request_id_in_cmo, "<30") \
               + format('Source ID: %s' % self.source_id, "<20") \
               + format('Request ID in source: %s' % self.request_id_in_source, "<33") \
               + format('Buffer ID: %s' % self.buffer_id, "<20") \
               + format('Device ID: %s' % self.device_id, "<15")
