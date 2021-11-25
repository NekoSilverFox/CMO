# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 16:57
# @Author  : Meng Jianing
# @FileName: buffer.py
# @Software: PyCharm
# @Versions: v0.1
# @Github  ：https://github.com/NekoSilverFox
# --------------------------------------------


class Buffer:
    num_buffer = 0  # 当前 CMO 中的缓冲区总数

    def __init__(self, timeline, priority=None):
        """ 初始化缓冲区

        :param timeline: 时间线
        :param priority: 本缓冲区的优先级，如果未指定则与此缓冲区的 ID 相同
        """
        Buffer.num_buffer += 1
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
        return format('[Buffer] ID: %s' % self.id, '<15') \
               + format('Priority: %s' % self.priority, '<15') \
               + format('Request in buffer: %s' %
                        (self.request_in_buffer.source.id.__str__() + "-" + self.request_in_buffer.request_id.__str__())
                        , '<35') \
               + format('Time push last request: %s' % self.request_push_time) \
               + format('Number request been: %s' % self.num_been_request, '<35') \
               + format('Serve time: %s' % self.serve_time, '<25')

    def push_request(self, request):
        """ 向缓冲区插入一个请求
        如果请求不为空或者缓冲区中现在无请求，则插入成功，返回 True；否则返回 False

        :param request: 要插入的请求
        :return: 如果请求不为空或者缓冲区中现在无请求，则插入成功，返回 True；否则返回 False
        """
        # 如果请求为空且当前缓冲区中有请求，不得再插入，故返回 False
        if request is None or self.request_in_buffer is not None:
            return False

        self.request_in_buffer = request
        self.request_push_time = self.timeline.get_time()
        self.num_been_request += 1
        return True

    def pop_request(self):
        # 如果当前缓冲区中无请求，返回 None
        if self.request_in_buffer is None:
            return None

        # 如果缓冲区中有请求，先将服务时间进行累加
        self.serve_time += (self.timeline.get_time - self.request_push_time)

        # 再将当前缓冲区置空，并返回缓冲区中的请求
        request = self.request_in_buffer
        self.request_in_buffer = None
        return request

