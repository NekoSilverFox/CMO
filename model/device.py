# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 16:59
# @Author  : Meng Jianing
# @FileName: device.py
# @Software: PyCharm
# @Versions: v0.1
# @Github  ：https://github.com/NekoSilverFox
# --------------------------------------------
from model.event import Event


class Device:
    """处理机"""

    num_device = 0  # static 当前 CMO 中的处理机总数
    num_vacant_device = 0  # static 当前 CMO 中的空闲的处理机总数

    def __init__(self, timeline, max_duration_handle=100, duration_lambda=0.5, priority=None):
        """ 初始化处理机

        :param timeline: 时间线
        :param max_duration_handle: **最大的处理时间**，即第一个请求所需的时间（*$MaxTime > 0$*），未指定则为默认为 100
        :param duration_lambda: `LAMBDA` - 参数，越接近 1，函数递减的就越快（$0 < LAMBDA < 1$），未指定则默认为 0.5
        :param priority: 本缓冲区的优先级，如果未指定则与此缓冲区的 ID 相同
        """

        Device.num_device += 1
        Device.num_vacant_device += 1
        self.id = Device.num_device     # 处理机 ID

        if priority is None:            # 处理机优先级
            self.priority = self.id
        else:
            self.priority = priority

        self.max_duration_handle = max_duration_handle  # **最大的处理时间**，即第一个请求所需的时间（*$MaxTime > 0$*）

        if duration_lambda < 0 or duration_lambda > 1:
            print('[ERROR] LAMBDA should between 0 and 1')
            exit(1)
        self.duration_lambda = duration_lambda  # LAMBDA` - 参数，越接近 1，函数递减的就越快（$0 < LAMBDA < 1$），未指定则默认为 0.5

        self.request_in_device = None   # 当前在处理机中的请求
        self.request_push_time = None   # 上一个/当前 请求进入处理机的时间
        self.request_done_time = None   # 当前请求处理结束的时间（未来）
        self.serve_time = 0             # 本处理机的服务时间（各请求在处理机中的停留时间总和）
        self.num_been_request = 0       # 本处理机中处理过的请求总数
        self.timeline = timeline        # 时间线（用户传入）

    def __str__(self):
        """ 返回说明当前处理机(Device)的字符串

        :return: 说明当前处理机(Device)的字符串
        """
        # 如果缓冲中没有请求的话在输出缓冲中请求的时候应该输出 None，而不应该去取值，去取值的话会报错
        request_source_id = None
        request_id_in_source = None
        if self.request_in_device is not None:
            request_source_id = self.request_in_device.source.request_id_in_source
            request_id_in_source = self.request_in_device.request_id

        return format('\033[31;1m[Device]\033[0m ID: %s' % self.id, '<30') \
               + format('Priority: %s' % self.priority, '<18') \
               + format('Request in buffer: %s' %
                        (request_source_id.__str__() + "-" + request_id_in_source.__str__())
                        , '<35') \
               + format('Time push last/this request: %s' % self.request_push_time, '<45') \
               + format('Time done last/this request: %s' % self.request_done_time, '<45') \
               + format('Number request been: %s' % self.num_been_request, '<35') \
               + format('Serve time: %s' % self.serve_time, '<25')

    @staticmethod
    def reset():
        """ 将所有 static 的属性恢复到默认值，谨慎调用！

        :return: 无
        """
        Device.num_device = 0
        Device.num_vacant_device = 0

    def duration_handle_this_request(self):
        """ 【时间段】处理当前请求所需的时长
           处理机的处理时间应该为**负指数增长**，即**越往后的请求，处理越快**

            ​	公式：

            ​	**$$ 处理时间 = MaxTime \cdot X^{-LAMBDA} $$**

            - `MaxTime` - **最大的处理时间**，即第一个请求所需的时间（*$MaxTime > 0$*）
            - `X` - 第几个请求（$X > 0, X∈Z $）
            - `LAMBDA` - 参数，越接近 1，函数递减的就越快（$0 < LAMBDA < 1$）

        :return: 处理当前请求所需的时长
        """
        # 如果没有处理过请求，直接返回 None
        if self.num_been_request == 0:
            return None

        return self.max_duration_handle \
               * (self.num_been_request ** (-1 * self.duration_lambda)) \
               * self.timeline.get_time_unit()

    def push_request(self, request):
        """ 向缓处理机插入一个请求
        如果请求不为空或者处理机中现在无请求，则插入成功，返回 True；否则返回 False

        :param request:
        :return:
        """
        # 如果请求为空且当前处理机中有请求，不得再插入，故返回 False
        if request is None or self.request_in_device is not None:
            return False

        # 将请求插入的动作写入日志
        event = Event(happen_time=self.timeline.get_time(),
                      event_type=Event.REQUEST_PUSH_IN_DEVICE,
                      request_id_in_cmo=request.request_id_in_cmo,
                      source_id=request.source.id,
                      request_id_in_source=request.request_id_in_source,
                      buffer_id=None,
                      device_id=self.id)
        self.timeline.add_event(event)

        Device.num_vacant_device -= 1
        self.num_been_request += 1
        self.request_in_device = request
        self.request_push_time = self.timeline.get_time()

        # 确定当前请求的处理结束时间
        self.request_done_time = self.request_push_time + self.duration_handle_this_request()
        # print(self.request_done_time)  # TODO
        return True

    def pop_request(self):
        """ 如果当前处理机中有请求且服务时间结束则从缓冲区中弹出当前请求（返回次请求），否则则返回 None

        :return: 处理完成的请求 或 None
        """
        # TODO 这是一个异常测试，如果当前处理机中有请求且当前时间大于了处理机应处理结束的时间。说明未能成功或未弹出请求
        # if (self.request_in_device is not None) and (self.timeline.get_time() > self.request_done_time):
        #     print(
        #         f'[WARNING] Request did not pop from this device! Device ID: {self.id:d}, '
        #         f'Request ID in CMO: {self.request_in_device.request_id_in_cmo:d}')

        # 如果当前处理机中无请求，或者未到该弹出的时间返回 None
        if (self.request_in_device is None) \
                or (self.timeline.get_time() < self.request_done_time):  # 因为存在精度的损失，可能会有1单位的时间的延迟，所以使用了小于号
            return None

        request = self.request_in_device

        # 将请求插入的动作写入日志
        event = Event(happen_time=self.timeline.get_time(),
                      event_type=Event.REQUEST_POP_FROM_DEVICE,
                      request_id_in_cmo=request.request_id_in_cmo,
                      source_id=request.source.id,
                      request_id_in_source=request.request_id_in_source,
                      buffer_id=None,
                      device_id=self.id)
        self.timeline.add_event(event)

        Device.num_vacant_device += 1
        self.serve_time += (self.timeline.get_time() - self.request_push_time)
        self.request_in_device = None
        return request
