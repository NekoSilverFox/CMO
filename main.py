# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 16:57
# @Author  : Meng Jianing
# @FileName: testTool.py
# @Software: PyCharm
# @Versions: v0.1
# @Github  ：https://github.com/NekoSilverFox
# --------------------------------------------
from model.timeLine import TimeLine
from model.source import Source
from model.buffer import Buffer
from model.device import Device
from function.testTool import *
from assist.format import LINE_LENGTH
from model.event import Event


if __name__ == '__main__':
    # tmp = Event(1, Event.REQUEST_CREATE, 2, 3, 4, 5, 6)
    # print(tmp)
    #
    # tmp = Event(1, Event.REQUEST_CREATE, 2, None, 4, 5, 6)
    # print(tmp)
    #
    # i = 1
    # print(i.__str__())
    #
    # r = Request(2, 1)
    # print(r)
    # r2 = Request(2, 3)
    # print(r2)

    # print('开始测试 TimeLine')

    # while True:
    #     tl = TimeLine(0.1)
    #     print(tl.get_time())
    #     tl.time_go()

    # tl = TimeLine()
    # copy_tl = tl
    #
    # print('当前【源】时间线的时间为：' + tl.get_time().__str__())
    # print('当前【拷贝】时间线的时间为：' + copy_tl.get_time().__str__())
    # tl.time_go()
    # tl.time_go()
    # tl.time_go()
    # print('--------------------时间增加------------------------------')
    # print('当前【源】时间线的时间为：' + tl.get_time().__str__())
    # print('当前【拷贝】时间线的时间为：' + copy_tl.get_time().__str__())
    #
    # print('--------------------测试------------------------------')



    # 确定要创建的各种的数量
    # source_num = int(input('Source 的数量：'))
    # buffer_num = int(input('Buffer 的数量：'))
    # device_num = int(input('Device 的数量：'))
    #
    # source_list = []
    # buffer_list = []
    # device_list = []
    #
    # # 循环创建源
    # i = 0
    # while i < source_num:
    #     i += 1
    #     source = Source(timeline, 10)
    #     source_list.append(source)
    #     print(source)
    #
    # while timeline.time_go():
    #     print('Time now: %s' % timeline.get_time())
    #     for source in source_list:
    #         source.create_request()
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""


    # 创建时间线
    print('*' * LINE_LENGTH)
    timeline = TimeLine()

    print('*' * LINE_LENGTH)
    source_list = create_source_list(timeline, 3, 30, 70)

    print('*' * LINE_LENGTH)
    buffer_list = create_buffer_list(timeline, 3)

    print('*' * LINE_LENGTH)
    device_list = create_device_list(timeline, 3, 60, 100, 0.4, 0.8)

    print('*' * LINE_LENGTH)
    print('\033[33;1m[INFO]\033[0m Start running')

    print('*' * LINE_LENGTH)
    while timeline.time_go():
        # 1. 产生请求
        for source in source_list:
            request = source.create_request()

            # 产生了请求，插入缓冲
            if request is not None:
                is_success = push_request_in_buffer_list(request, buffer_list)

                # 如果未插入成功，代表缓冲和处理机都处在繁忙状态，该请求被取消。将事件写入到 timeline 的日志
                if is_success is False:
                    event = Event(happen_time=timeline.get_time(),
                                  event_type=Event.REQUEST_CANCEL,
                                  source_id=request.source.id,
                                  buffer_id=None,
                                  device_id=None,
                                  request_id_in_cmo=request.request_id_in_cmo,
                                  request_id_in_source=request.request_id_in_source)
                    timeline.add_event(event)


