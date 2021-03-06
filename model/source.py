# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 16:56
# @Author  : Meng Jianing
# @FileName: source.py
# @Software: PyCharm
# @Versions: v0.1
# @Github  ：https://github.com/NekoSilverFox
# --------------------------------------------
from model.request import Request
from model.event import Event


class Source:
    """源 —— 用于生成请求"""

    num_source = 0  # 记录创建了的源的总数

    def __init__(self, timeline, interval, priority=None):
        """ 初始化源

        :param interval: 生成请求之间的间隔
        :param priority: 本源的优先级，如果未指定则与此源的 ID 相同
        """
        Source.num_source += 1
        self.id = Source.num_source     # 本源的ID

        if priority is None:
            self.priority = self.id     # 本源的优先级
        else:
            self.priority = priority    # 本源的优先级

        self.interval = interval        # 生成请求之间的间隔为几个时间单位
        self.timeline = timeline        # 时间线
        self.num_request = 0            # 本源生成的请求数量
        self.enable = True              # 是否启动当前源（默认为 True 即启动）
        self.time_create_next_request \
            = self.timeline.get_time() + self.interval * self.timeline.get_time_unit()  # 生成下一个请求的时间

    def __str__(self):
        """ 返回说明当前源(Source)的字符串

        :return: 说明当前源(Source)的字符串
        """
        return format('\033[32;1m[Source]\033[0m ID: %s' % self.id, '<30') \
               + format('Priority: %s' % self.priority, '<18') \
               + format('Interval: %s' % self.interval, '<20') \
               + format('Number created request: %s' % self.num_request, '<33') \
               + format('Next request create time: %s' % self.time_create_next_request, '<35') \
               + format('Enable: %s' % self.enable, '<15')

    @staticmethod
    def reset():
        """ 将所有 static 的属性恢复到默认值，谨慎调用！

        :return: 无
        """
        Source.num_source = 0

    def create_request(self):
        """生成请求
        如果当前的时间和本源生成下一个请求的时间（` self`.time_create_next_request` ）一致则生成请求，并返回生成的请求（Request）对象，否则返回 None
        :return: Request对象 或 None
        """
        # CMO的当前时间和本源生成下一个请求的时间（`self`.time_create_next_request` ）不一致，返回
        if self.time_create_next_request != self.timeline.get_time():
            return None

        self.num_request += 1
        request = Request(self, self.num_request)
        # 更新生成下一个请求的时间
        self.time_create_next_request += self.interval * self.timeline.get_time_unit()

        # 将请求插入的动作写入日志
        event = Event(happen_time=self.timeline.get_time(),
                      event_type=Event.REQUEST_CREATE,
                      request_id_in_cmo=request.request_id_in_cmo,
                      source_id=request.source.id,
                      request_id_in_source=request.request_id_in_source,
                      buffer_id=None,
                      device_id=None)
        self.timeline.add_event(event)

        return request
