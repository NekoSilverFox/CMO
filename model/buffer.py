# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 16:57
# @Author  : Meng Jianing
# @FileName: buffer.py
# @Software: PyCharm
# @Versions: v0.1
# @Github  ：https://github.com/NekoSilverFox
# --------------------------------------------
from model.event import Event


class Buffer:
    """缓冲区"""

    num_buffer = 0  # 当前 CMO 中的缓冲区总数
    num_vacant_buffer = 0  # static 当前 CMO 中的空闲的处理机总数

    def __init__(self, timeline, priority=None):
        """ 初始化缓冲区

        :param timeline: 时间线
        :param priority: 本缓冲区的优先级，如果未指定则与此缓冲区的 ID 相同
        """
        Buffer.num_buffer += 1
        Buffer.num_vacant_buffer += 1
        self.id = Buffer.num_buffer     # 缓冲区 ID

        if priority is None:            # 缓冲区优先级
            self.priority = self.id
        else:
            self.priority = priority

        self.request_in_buffer = None   # 当前在缓冲区中的请求
        self.request_push_time = None   # 上一个/当前 请求进入缓冲区的时间
        self.num_been_request = 0       # 本缓冲区中存留过的请求总数
        self.serve_time = 0             # 本缓冲区的服务时间（各请求在缓冲区的停留时间总和）
        self.timeline = timeline        # 时间线

    def __str__(self):
        """ 返回说明当前缓冲区(Buffer)的字符串

        :return: 说明当前缓冲区(Buffer)的字符串
        """
        # 如果缓冲中没有请求的话在输出缓冲中请求的时候应该输出 None，而不应该去取值，去取值的话会报错
        request_source_id = None
        request_id_in_source = None
        if self.request_in_buffer is not None:
            request_source_id = self.request_in_buffer.source.request_id_in_source
            request_id_in_source = self.request_in_buffer.request_id

        return format('\033[34;1m[Buffer]\033[0m ID: %s' % self.id, '<30') \
               + format('Priority: %s' % self.priority, '<18') \
               + format('Request in buffer: %s' %
                        (request_source_id.__str__() + "-" + request_id_in_source.__str__()), '<35') \
               + format('Time push last/this request: %s' % self.request_push_time, '<45') \
               + format('Number request been: %s' % self.num_been_request, '<35') \
               + format('Serve time: %s' % self.serve_time, '<25')

    @staticmethod
    def reset():
        """ 将所有 static 的属性恢复到默认值，谨慎调用！

        :return: 无
        """
        Buffer.num_buffer = 0
        Buffer.num_vacant_buffer = 0

    def push_request(self, request):
        """ 向缓冲区插入一个请求
        如果请求不为空或者缓冲区中现在无请求，则插入成功，返回 True；否则返回 False

        :param request: 要插入的请求
        :return: 如果请求不为空或者缓冲区中现在无请求，则插入成功，返回 True；否则返回 False
        """
        # 如果请求为空且当前缓冲区中有请求，不得再插入，故返回 False
        if request is None or self.request_in_buffer is not None:
            return False

        Buffer.num_vacant_buffer -= 1
        self.request_in_buffer = request
        self.request_push_time = self.timeline.get_time()
        self.num_been_request += 1

        # 将请求插入的动作写入日志
        event = Event(happen_time=self.timeline.get_time(),
                      event_type=Event.REQUEST_PUSH_IN_BUFFER,
                      request_id_in_cmo=request.request_id_in_cmo,
                      source_id=request.source.id,
                      request_id_in_source=request.request_id_in_source,
                      buffer_id=self.id,
                      device_id=None)
        self.timeline.add_event(event)

        return True

    def pop_request(self):
        """ 如果当前缓冲区中有请求，则弹出当前请求（返回Request），否则返回 None

        :return: Request请求 或 None
        """
        # 如果当前缓冲区中无请求，返回 None
        if self.request_in_buffer is None:
            return None

        request = self.request_in_buffer

        Buffer.num_vacant_buffer += 1

        # 如果缓冲区中有请求，先将服务时间进行累加
        self.serve_time += (self.timeline.get_time() - self.request_push_time)

        # 再将当前缓冲区置空，并返回缓冲区中的请求
        self.request_in_buffer = None

        # 将请求插入的动作写入日志
        event = Event(happen_time=self.timeline.get_time(),
                      event_type=Event.REQUEST_POP_FROM_BUFFER,
                      request_id_in_cmo=request.request_id_in_cmo,
                      source_id=request.source.id,
                      request_id_in_source=request.request_id_in_source,
                      buffer_id=self.id,
                      device_id=None)
        self.timeline.add_event(event)
        return request
