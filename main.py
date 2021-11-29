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
from colorPrinter.colorPrinter import *


def model_bank():
    # 创建时间线
    print('*' * LINE_LENGTH)
    timeline = TimeLine()
    timeline.debug_off()
    timeline.print_event_off()
    print('*' * LINE_LENGTH)

    money_buffer = 500000
    money_device = 2000000
    max_num_buffer = 10
    max_num_device = 10
    tmp_num_buffer = 0

    while tmp_num_buffer < max_num_buffer:
        tmp_num_buffer += 1
        tmp_num_device = 0

        while tmp_num_device < max_num_device:
            tmp_num_device += 1

            source_list = []
            source_list.clear()
            source_list.append(Source(timeline, 10))
            source_list.append(Source(timeline, 30))
            source_list.append(Source(timeline, 20))
            source_list.append(Source(timeline, 15))
            source_list.append(Source(timeline, 50))

            buffer_list = create_buffer_list(timeline, tmp_num_buffer, False)
            # device_list = create_device_list(timeline, tmp_num_device, 60, 60, 0.1, 0.1, False)
            device_list = create_device_list(timeline, tmp_num_device, 60, 90, 0.5, 0.5, False)

            running_model(timeline, source_list, buffer_list, device_list, 300)

            # 获取总等待时长
            all_wait_time = 0
            for buffer in buffer_list:
                all_wait_time += buffer.serve_time
            # 获取总平均等待时长
            avg_wait_time = all_wait_time / (Request.num_request - Request.num_cancel_request)

            # 获取总平均服务时长
            all_handle_time = 0
            for device in device_list:
                all_handle_time += device.serve_time
            # 获取总平均服务时长
            avg_handle_time = all_handle_time / (Request.num_request - Request.num_cancel_request)

            str_num_buffer = ColorPrinter.get_color_string('Num buffer: ' + tmp_num_buffer.__str__(), ForeColor.BLUE, ShowType.HIGHLIGHT)
            str_num_device = ColorPrinter.get_color_string('Num device: ' + tmp_num_device.__str__(), ForeColor.RED, ShowType.HIGHLIGHT)
            str_avg_wait_time = '总平均等待时长: ' + round(avg_wait_time, 4).__str__()
            str_avg_handle_time = '总平均服务时长: ' + round(avg_handle_time, 4).__str__()
            str_p_cancel = '请求取消概率: ' + round(Request.num_cancel_request / Request.num_request, 5).__str__()
            str_money_buffer = '等候区花费: ' + (money_buffer * tmp_num_buffer).__str__()
            str_money_device = '窗口花费: ' + (money_device * tmp_num_device).__str__()
            str_all_money = '总花费: ' + ((money_buffer * tmp_num_buffer) + (money_device * tmp_num_device)).__str__()

            mix_str = format(str_num_buffer, '<30') \
               + format(str_num_device, '<30') \
               + format(str_avg_wait_time, '<20') \
               + format(str_avg_handle_time, '<20') \
               + format(str_p_cancel, '<20') \
               + format(str_money_buffer, '<20') \
               + format(str_money_device, '<20') \
               + format(str_all_money, '<20')
            print(mix_str)

            # print(device_info_table_ru(timeline, device_list))
            # print(source_info_table_ru(timeline, source_list))

            # print('#' * LINE_LENGTH)

            timeline.reset()
            Request.reset()
            Source.reset()
            Buffer.reset()
            Device.reset()
            source_list.clear()
            buffer_list.clear()
            device_list.clear()
    pass


def running_model(timeline, source_list, buffer_list, device_list, num_need_request):
    """ 根据提供的时间线、源列表、缓冲区列表、处理机列表开始模拟

    :param timeline: 时间线
    :param source_list: 包含有多个源的 list列表
    :param buffer_list: 包含有多个缓冲区的 list列表
    :param device_list: 包含有多个处理机的 list列表
    :param num_need_request: 需要生成请求的数量
    :return: 无
    """
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
        # print(timeline.get_time())  # TODO

        # 4. 如果缓冲和处理机都为空，并且需要生成的请求数量和生成的请求数量相等，则程序结束
        if (Device.num_vacant_device == Device.num_device) \
                and (Buffer.num_vacant_buffer == Buffer.num_buffer) \
                and (Request.num_request >= num_need_request):
            # print(ColorPrinter.get_color_string('[INFO] Model has down', ForeColor.GREEN, ShowType.HIGHLIGHT))
            break

        # 3. 如果请求数量未达到就查看是否有需要产生的请求，如果有则插入缓冲
        if Request.num_request != num_need_request:
            for source in source_list:
                request = source.create_request()

                # 3.1 产生了请求，插入缓冲
                if request is not None:
                    is_success = push_request_in_buffer_list(request, buffer_list)

                    # 3.2 如果未插入成功，代表缓冲和处理机都处在繁忙状态，该请求被取消。将事件写入到 timeline 的日志
                    if is_success is False:
                        Request.num_cancel_request += 1
                        event = Event(happen_time=timeline.get_time(),
                                      event_type=Event.REQUEST_CANCEL,
                                      source_id=request.source.id,
                                      buffer_id=None,
                                      device_id=None,
                                      request_id_in_cmo=request.request_id_in_cmo,
                                      request_id_in_source=request.request_id_in_source)
                        timeline.add_event(event)
    pass

if __name__ == '__main__':
    model_bank()
    exit(0)
"""
    ColorPrinter.color_print('*' * LINE_LENGTH, ForeColor.PURPLE, ShowType.HIGHLIGHT)
    ColorPrinter.color_print('Выбор режима:\n', ShowType.HIGHLIGHT)
    ColorPrinter.color_print('\t1 - автоматический\n', ForeColor.GREEN, ShowType.HIGHLIGHT)
    ColorPrinter.color_print('\t2 - пошаговый\n', ForeColor.BLUE, ShowType.HIGHLIGHT)
    choose_mode = int(input('>>> '))
    if choose_mode != 1 and choose_mode != 2:
        ColorPrinter.color_print('Please choose `1` or `2` !')
        exit(1)
    ColorPrinter.color_print('*' * LINE_LENGTH, ForeColor.PURPLE, ShowType.HIGHLIGHT)

    source_num = int(input('Введите количество '
                           + ColorPrinter.get_color_string('источников', ForeColor.GREEN, ShowType.HIGHLIGHT) + ': '))

    buffer_num = int(input('Введите количество '
                           + ColorPrinter.get_color_string('буферов', ForeColor.BLUE, ShowType.HIGHLIGHT) + ': '))

    device_num = int(input('Введите количество '
                           + ColorPrinter.get_color_string('приборов', ForeColor.RED, ShowType.HIGHLIGHT) + ': '))

    num_need_request = int(input('Введите количество '
                           + ColorPrinter.get_color_string('моделируемых заявок', ForeColor.PURPLE, ShowType.HIGHLIGHT) + ': '))

    # 创建时间线
    print('*' * LINE_LENGTH)
    timeline = TimeLine()
    if choose_mode == 1:
        timeline.debug_off()
    elif choose_mode == 2:
        timeline.debug_on()
    else:
        pass

    print('*' * LINE_LENGTH)
    print('\033[33;1m[INFO]\033[0m CMO Start running...\n')
    print('☩ Settings: ')
    if timeline.is_debug():
        print('\tDebug mode\t\t' + ColorPrinter.get_color_string('ON', ForeColor.GREEN, ShowType.HIGHLIGHT))
    else:
        print('\tDebug mode\t\t' + ColorPrinter.get_color_string('OFF', ForeColor.RED, ShowType.HIGHLIGHT))

    if timeline.is_print_event():
        print('\tPrint event\t\t' + ColorPrinter.get_color_string('ON', ForeColor.GREEN, ShowType.HIGHLIGHT))
    else:
        print('\tPrint event\t\t' + ColorPrinter.get_color_string('OFF', ForeColor.RED, ShowType.HIGHLIGHT))

    print('*' * LINE_LENGTH)
    source_list = create_source_list(timeline, source_num, 30, 70)

    print('*' * LINE_LENGTH)
    buffer_list = create_buffer_list(timeline, buffer_num)

    print('*' * LINE_LENGTH)
    device_list = create_device_list(timeline, device_num, 60, 100, 0.4, 0.8)

    print('*' * LINE_LENGTH)
    running_model(timeline=timeline,
                  source_list=source_list,
                  buffer_list=buffer_list,
                  device_list=device_list,
                  num_need_request=num_need_request)

    print(source_info_table_ru(timeline, source_list))
    print(device_info_table_ru(timeline, device_list))
    pass
"""

    # 几个源中产生请求在CMO中的ID
    # print('*' * LINE_LENGTH)
    # print('几个源中产生请求在CMO中的ID:')
    # for source in source_list:
    #     request_cmo_id_list = get_request_cmo_id_list_by_source(timeline, source)
    #     print(request_cmo_id_list)
    #
    # # 几个源中请求在缓冲中的等待时长
    # print('*' * LINE_LENGTH)
    # print('个源中请求在缓冲中的等待时长:')
    # for source in source_list:
    #     wait_time_list = get_request_wait_time_list_in_buffer_by_source(timeline, source)
    #     print(wait_time_list)
    #
    # # 几个源中请求在处理机中的服务时长
    # print('*' * LINE_LENGTH)
    # print('几个源中请求在处理机中的服务时长:')
    # for source in source_list:
    #     handle_time_list = get_request_handle_time_list_in_device_by_source(timeline, source)
    #     print(handle_time_list)
    #
    # # 几个源中请求在CMO中的生命周期
    # print('*' * LINE_LENGTH)
    # print('几个源中请求在CMO中的生命周期:')
    # for source in source_list:
    #     live_time_list = get_request_live_time_list_in_device_by_source(timeline, source)
    #     print(live_time_list)
    #
    # # 几个源中请求在CMO中被取消的请求
    # print('*' * LINE_LENGTH)
    # print('几个源中请求在CMO中被取消的请求:')
    # for source in source_list:
    #     live_time_list = get_request_cancel_list_in_device_by_source(timeline, source)
    #     print(live_time_list)
