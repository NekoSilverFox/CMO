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
from model.request import Request
from function.testTool import *
from assist.format import LINE_LENGTH
from model.event import Event
from function.tablePrinter import *

if __name__ == '__main__':
    # 创建时间线
    print('*' * LINE_LENGTH)
    timeline = TimeLine()

    print('*' * LINE_LENGTH)
    source_list = create_source_list(timeline, 10, 30, 70)

    print('*' * LINE_LENGTH)
    buffer_list = create_buffer_list(timeline, 3)

    print('*' * LINE_LENGTH)
    device_list = create_device_list(timeline, 3, 60, 100, 0.4, 0.8)

    print('*' * LINE_LENGTH)
    print('\033[33;1m[INFO]\033[0m Start running')

    num_need_request = 50

    print('*' * LINE_LENGTH)
    while True:
        # 1. 查看处理机中是否有需要处理结束的请求
        done_request_in_device_list(device_list)

        # 2. 查看缓冲区中时候是否有需要放入处理机的
        # 直到 处理机全部被占用(没有空闲处理机) 或者 缓冲区全为空
        # while 循环：     如果处理机没被占满      并且            缓冲区不全为空
        while (Device.num_vacant_device != 0) and (Buffer.num_vacant_buffer != Buffer.num_buffer):
            # 选择应该弹出请求的 Buffer
            buffer_should_pop = choose_buffer_from_buffer_list(buffer_list)
            request = buffer_should_pop.pop_request()

            # 插入处理机
            push_request_in_device_list(request, device_list)

        timeline.time_go()

        # 如果缓冲和处理机都为空，并且需要生成的请求数量和生成的请求数量相等，则程序结束
        if (Device.num_vacant_device == Device.num_device) \
                and (Buffer.num_vacant_buffer == Buffer.num_buffer) \
                and (Request.num_request == num_need_request):
            break

        # 3. 如果请求数量未达到就查看是否有需要产生的请求，如果有则插入缓冲
        if Request.num_request != num_need_request:
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

    print(source_info_table_cn(timeline, source_list))

    # 几个源中产生请求在CMO中的ID
    print('*' * LINE_LENGTH)
    print('几个源中产生请求在CMO中的ID:')
    for source in source_list:
        request_cmo_id_list = get_request_cmo_id_list_by_source(timeline, source)
        print(request_cmo_id_list)

    # 几个源中请求在缓冲中的等待时长
    print('*' * LINE_LENGTH)
    print('个源中请求在缓冲中的等待时长:')
    for source in source_list:
        wait_time_list = get_request_wait_time_list_in_buffer_by_source(timeline, source)
        print(wait_time_list)

    # 几个源中请求在处理机中的服务时长
    print('*' * LINE_LENGTH)
    print('几个源中请求在处理机中的服务时长:')
    for source in source_list:
        handle_time_list = get_request_handle_time_list_in_device_by_source(timeline, source)
        print(handle_time_list)

    # 几个源中请求在CMO中的生命周期
    print('*' * LINE_LENGTH)
    print('几个源中请求在CMO中的生命周期:')
    for source in source_list:
        live_time_list = get_request_live_time_list_in_device_by_source(timeline, source)
        print(live_time_list)

    # 几个源中请求在CMO中被取消的请求
    print('*' * LINE_LENGTH)
    print('几个源中请求在CMO中被取消的请求:')
    for source in source_list:
        live_time_list = get_request_cancel_list_in_device_by_source(timeline, source)
        print(live_time_list)
