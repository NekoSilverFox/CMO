# -*- coding: utf-8 -*-
# @Time    : 2021/11/28 0:06
# @Author  : Meng Jianing
# @FileName: tablePrinter.py
# @Software: PyCharm
# @Versions: v0.1
# @Github  ：https://github.com/NekoSilverFox
# --------------------------------------------

from colorPrinter.colorPrinter import *
from function.testTool import *

SOURCE_TABLE_LINE_LENGTH = 150
DEVICE_TABLE_LINE_LENGTH = 80


def source_info_table_cn(timeline, source_list):
    """ 请在请求全部处理完成后调用！
        以表格的形式输出各个源生成请求的统计信息：
        - 源 ID
        - 该源产生的总请求数
        - 该源产生的取消率
        - 该源产生所有请求的停留总时间
        - 该源产生所有请求在缓冲中等待时间
        - 该源产生的所有请求服务总时间
        - 该源产生所有请求的等待时间的方差
        - 该源产生所有请求的服务时间的方差
    -
    :param timeline: 时间线
    :param source_list: 包含有多个源的列表
    :return: 带有统计信息的字符串
    """
    if timeline is None or source_list is None:
        return None

    # 如果程序正确，那么 请求停留总时间 = 缓冲中等待时间 + 服务时间
    str_source_table = ('\n┏' + '┅' * SOURCE_TABLE_LINE_LENGTH) + '┓\n' \
                       + '┇' + format(ColorPrinter.get_color_string(
                            string='Source info table',
                            fore_color=ForeColor.GREEN,
                            show_type=ShowType.HIGHLIGHT), ('^' + (SOURCE_TABLE_LINE_LENGTH + 11).__str__())) + '┇\n' \
                       + ('┣' + '┅' * SOURCE_TABLE_LINE_LENGTH) + '┫\n' \
                       + '┇' + format(ColorPrinter.get_color_string('Source ID', ShowType.HIGHLIGHT), '^21') \
                       + '┇' + format(ColorPrinter.get_color_string('生成的请求数', ShowType.HIGHLIGHT), '^21') \
                       + '┇' + format(ColorPrinter.get_color_string('请求的取消率', ShowType.HIGHLIGHT), '^23') \
                       + '┇' + format(ColorPrinter.get_color_string('请求停留总时间', ShowType.HIGHLIGHT), '^24') \
                       + '┇' + format(ColorPrinter.get_color_string('缓冲中等待时间', ShowType.HIGHLIGHT), '^24') \
                       + '┇' + format(ColorPrinter.get_color_string('服务时间', ShowType.HIGHLIGHT), '^24') \
                       + '┇' + format(ColorPrinter.get_color_string('等待时间的方差', ShowType.HIGHLIGHT), '^23') \
                       + '┇' + format(ColorPrinter.get_color_string('服务时间的方差', ShowType.HIGHLIGHT), '^23') + '┇\n' \
                       + ('┣' + '┅' * SOURCE_TABLE_LINE_LENGTH) + '┫\n' \

    for source in source_list:
        # 源 ID
        source_id = source.id

        # 这个源生成的请求数量
        num_request = source.num_request

        # 这个源被取消请求的数量
        num_cancel_request = len(get_request_cancel_list_in_device_by_source(timeline, source))

        # 这个源生成请求被取消的概率
        probability_cancel = num_cancel_request / num_request

        # 这个源生成请求的声明周期总和
        all_request_live_time = 0

        # 这个源生成请求在 buffer 中的总停留时长
        all_request_wait_time_in_buffer = 0

        # 这个源生成请求在 处理机中的总处理时长
        all_request_handle_time = 0

        # 这个源生成请求在 Buffer 中的等待时长的【方差】
        variance_wait_time = 0

        # 这个源生成请求在 Device 中的服务时长的【方差】
        variance_handle_time = 0

        # 累加这个源生成请求的总生命周期
        live_time_list = get_request_live_time_list_in_device_by_source(timeline, source)
        for event_live_time in live_time_list:
            all_request_live_time += event_live_time[2]

        # 累加这个源生成请求的总等待时长
        live_wait_time_list = get_request_wait_time_list_in_buffer_by_source(timeline, source)
        for event_wait_time in live_wait_time_list:
            all_request_wait_time_in_buffer += event_wait_time[2]

        # 累加这个源生成请求的总处理时间
        live_handle_time_list = get_request_handle_time_list_in_device_by_source(timeline, source)
        for event_handle_time in live_handle_time_list:
            all_request_handle_time += event_handle_time[2]

        # 计算这个源生成请求在 Buffer 中的等待时长的【方差】
        # 会有这种情况：生成的请求全部被取消！所以说要对除零做判断！
        if num_request == num_cancel_request:
            variance_wait_time = 0
        else:
            ave_wait_time = all_request_wait_time_in_buffer / (num_request - num_cancel_request)  # 在 Buffer 中的平均等待时长
            for event_wait_time in live_wait_time_list:
                variance_wait_time += ((event_wait_time[2] - ave_wait_time) ** 2)
            variance_wait_time /= (num_request - num_cancel_request)

        # 计算这个源生成请求在 Device 中的处理时长的【方差】
        # 会有这种情况：生成的请求全部被取消！所以说要对除零做判断！
        if num_request == num_cancel_request:
            variance_handle_time = 0
        else:
            ave_handle_time = all_request_handle_time / (num_request - num_cancel_request)  # 在 Device 中的平均等待时长
            for event_handle_time in live_handle_time_list:
                variance_handle_time += ((event_handle_time[2] - ave_handle_time) ** 2)
            variance_handle_time /= (num_request - num_cancel_request)

        str_source_table += (
          '┇' + format(ColorPrinter.get_color_string('И' + source_id.__str__(), ShowType.HIGHLIGHT), '^21') \
          + '┇' + format(ColorPrinter.get_color_string(num_request.__str__()), '^17') \
          + '┇' + format(ColorPrinter.get_color_string((round((probability_cancel * 100), 5).__str__() + ' %')), '^18') \
          + '┇' + format(ColorPrinter.get_color_string(all_request_live_time.__str__()), '^18') \
          + '┇' + format(ColorPrinter.get_color_string(all_request_wait_time_in_buffer.__str__()), '^18') \
          + '┇' + format(ColorPrinter.get_color_string(all_request_handle_time.__str__()), '^18') \
          + '┇' + format(ColorPrinter.get_color_string((round(variance_wait_time, 5)).__str__()), '^22') \
          + '┇' + format(ColorPrinter.get_color_string((round(variance_handle_time, 5)).__str__()), '^21') + '┇\n' \
          + ('┣' + '┅' * SOURCE_TABLE_LINE_LENGTH) + '┫\n'
            )

    return str_source_table


def device_info_table_cn(timeline, device_list):
    """ 以表格的形式输出各个处理机的统计信息：
        - 处理机 ID
        - 处理总时长
        - 处理过的请求数
        - 使用率

    :param timeline: 时间线
    :param device_list: 包含有多个处理机的列表
    :return: 带有统计信息的字符串
    """
    if timeline is None or device_list is None:
        return None

    # 如果程序正确，那么 请求停留总时间 = 缓冲中等待时间 + 服务时间
    str_device_table = (('┏' + '┅' * DEVICE_TABLE_LINE_LENGTH) + '┓\n' \
                       + '┇' + format(ColorPrinter.get_color_string(
                            string='Device info table',
                            fore_color=ForeColor.BLUE,
                            show_type=ShowType.HIGHLIGHT), ('^' + (DEVICE_TABLE_LINE_LENGTH + 11).__str__())) + '┇\n' \
                       + ('┣' + '┅' * DEVICE_TABLE_LINE_LENGTH) + '┫\n' \
                       + '┇' + format(ColorPrinter.get_color_string('Device ID', ShowType.HIGHLIGHT), '^25') \
                       + '┇' + format(ColorPrinter.get_color_string('处理总时长', ShowType.HIGHLIGHT), '^28') \
                       + '┇' + format(ColorPrinter.get_color_string('处理过的请求数', ShowType.HIGHLIGHT), '^25') \
                       + '┇' + format(ColorPrinter.get_color_string('使用率', ShowType.HIGHLIGHT), '^25') + '┇\n' \
                       + ('┣' + '┅' * DEVICE_TABLE_LINE_LENGTH) + '┫\n'
                        )

    for device in device_list:
        # 处理机 ID
        device_id = device.id

        # 处理总时长
        serve_time = device.serve_time

        # 处理过的请求数
        num_been_server_request = device.num_been_request

        # 使用率
        usage_rate = device.serve_time / timeline.get_time()

        str_device_table += (
          '┇' + format(ColorPrinter.get_color_string('П' + device_id.__str__(), ShowType.HIGHLIGHT), '^25') \
          + '┇' + format(ColorPrinter.get_color_string(serve_time.__str__()), '^22') \
          + '┇' + format(ColorPrinter.get_color_string(num_been_server_request.__str__()), '^22') \
          + '┇' + format(ColorPrinter.get_color_string((round(usage_rate, 5)).__str__()), '^18') + '┇\n' \
          + ('┣' + '┅' * DEVICE_TABLE_LINE_LENGTH) + '┫\n'
            )

    return str_device_table


def source_info_table_ru(timeline, source_list):
    """ 请在请求全部处理完成后调用！
        以表格的形式输出各个源生成请求的统计信息：
        - 源 ID
        - 该源产生的总请求数
        - 该源产生的取消率
        - 该源产生所有请求的停留总时间
        - 该源产生所有请求在缓冲中等待时间
        - 该源产生的所有请求服务总时间
        - 该源产生所有请求的等待时间的方差
        - 该源产生所有请求的服务时间的方差

    :param timeline: 时间线
    :param source_list: 包含有多个源的列表
    :return: 带有统计信息的字符串
    """
    if timeline is None or source_list is None:
        return None

    # 如果程序正确，那么 请求停留总时间 = 缓冲中等待时间 + 服务时间
    str_source_table = ('\n┏' + '┅' * SOURCE_TABLE_LINE_LENGTH) + '┓\n' \
                       + '┇' + format(ColorPrinter.get_color_string(
                            string='Source info table',
                            fore_color=ForeColor.GREEN,
                            show_type=ShowType.HIGHLIGHT), ('^' + (SOURCE_TABLE_LINE_LENGTH + 11).__str__())) + '┇\n' \
                       + ('┣' + '┅' * SOURCE_TABLE_LINE_LENGTH) + '┫\n' \
                       + '┇' + format(ColorPrinter.get_color_string('Источник', ShowType.HIGHLIGHT), '^21') \
                       + '┇' + format(ColorPrinter.get_color_string('Кол-во заявок', ShowType.HIGHLIGHT), '^27') \
                       + '┇' + format(ColorPrinter.get_color_string('P отказа', ShowType.HIGHLIGHT), '^28') \
                       + '┇' + format(ColorPrinter.get_color_string('Т пребывания', ShowType.HIGHLIGHT), '^28') \
                       + '┇' + format(ColorPrinter.get_color_string('Т ожидания', ShowType.HIGHLIGHT), '^28') \
                       + '┇' + format(ColorPrinter.get_color_string('Т обслуживания', ShowType.HIGHLIGHT), '^28') \
                       + '┇' + format(ColorPrinter.get_color_string('Д ожидания', ShowType.HIGHLIGHT), '^32') \
                       + '┇' + format(ColorPrinter.get_color_string('Д обслуживания', ShowType.HIGHLIGHT), '^31') + '┇\n' \
                       + ('┣' + '┅' * SOURCE_TABLE_LINE_LENGTH) + '┫\n'

    for source in source_list:
        # 源 ID
        source_id = source.id

        # 这个源生成的请求数量
        num_request = source.num_request

        # 这个源被取消请求的数量
        num_cancel_request = len(get_request_cancel_list_in_device_by_source(timeline, source))

        # 这个源生成请求被取消的概率
        probability_cancel = num_cancel_request / num_request

        # 这个源生成请求的声明周期总和
        all_request_live_time = 0

        # 这个源生成请求在 buffer 中的总停留时长
        all_request_wait_time_in_buffer = 0

        # 这个源生成请求在 处理机中的总处理时长
        all_request_handle_time = 0

        # 这个源生成请求在 Buffer 中的等待时长的【方差】
        variance_wait_time = 0

        # 这个源生成请求在 Device 中的服务时长的【方差】
        variance_handle_time = 0

        # 累加这个源生成请求的总生命周期
        live_time_list = get_request_live_time_list_in_device_by_source(timeline, source)
        for event_live_time in live_time_list:
            all_request_live_time += event_live_time[2]

        # 累加这个源生成请求的总等待时长
        live_wait_time_list = get_request_wait_time_list_in_buffer_by_source(timeline, source)
        for event_wait_time in live_wait_time_list:
            all_request_wait_time_in_buffer += event_wait_time[2]

        # 累加这个源生成请求的总处理时间
        live_handle_time_list = get_request_handle_time_list_in_device_by_source(timeline, source)
        for event_handle_time in live_handle_time_list:
            all_request_handle_time += event_handle_time[2]

        # 计算这个源生成请求在 Buffer 中的等待时长的【方差】
        # 会有这种情况：生成的请求全部被取消！所以说要对除零做判断！
        if num_request == num_cancel_request:
            variance_wait_time = 0
        else:
            ave_wait_time = all_request_wait_time_in_buffer / (num_request - num_cancel_request)  # 在 Buffer 中的平均等待时长
            for event_wait_time in live_wait_time_list:
                variance_wait_time += ((event_wait_time[2] - ave_wait_time) ** 2)
            variance_wait_time /= (num_request - num_cancel_request)

        # 计算这个源生成请求在 Device 中的处理时长的【方差】
        # 会有这种情况：生成的请求全部被取消！所以说要对除零做判断！
        if num_request == num_cancel_request:
            variance_handle_time = 0
        else:
            ave_handle_time = all_request_handle_time / (num_request - num_cancel_request)  # 在 Device 中的平均等待时长
            for event_handle_time in live_handle_time_list:
                variance_handle_time += ((event_handle_time[2] - ave_handle_time) ** 2)
            variance_handle_time /= (num_request - num_cancel_request)

        str_source_table += (
          '┇' + format(ColorPrinter.get_color_string('И' + source_id.__str__(), ShowType.HIGHLIGHT), '^21') \
          + '┇' + format(ColorPrinter.get_color_string(num_request.__str__()), '^17') \
          + '┇' + format(ColorPrinter.get_color_string((round((probability_cancel * 100), 5).__str__() + ' %')), '^18') \
          + '┇' + format(ColorPrinter.get_color_string(all_request_live_time.__str__()), '^18') \
          + '┇' + format(ColorPrinter.get_color_string(all_request_wait_time_in_buffer.__str__()), '^18') \
          + '┇' + format(ColorPrinter.get_color_string(all_request_handle_time.__str__()), '^18') \
          + '┇' + format(ColorPrinter.get_color_string((round(variance_wait_time, 5)).__str__()), '^22') \
          + '┇' + format(ColorPrinter.get_color_string((round(variance_handle_time, 5)).__str__()), '^21') + '┇\n' \
          + ('┣' + '┅' * SOURCE_TABLE_LINE_LENGTH) + '┫\n'
            )

    return str_source_table


def device_info_table_ru(timeline, device_list):
    """ 以表格的形式输出各个处理机的统计信息：
        - 处理机 ID
        - 处理总时长
        - 处理过的请求数
        - 使用率

    :param timeline: 时间线
    :param device_list: 包含有多个处理机的列表
    :return: 带有统计信息的字符串
    """
    if timeline is None or device_list is None:
        return None

    # 如果程序正确，那么 请求停留总时间 = 缓冲中等待时间 + 服务时间
    str_device_table = (('┏' + '┅' * DEVICE_TABLE_LINE_LENGTH) + '┓\n' \
                       + '┇' + format(ColorPrinter.get_color_string(
                            string='Device info table',
                            fore_color=ForeColor.BLUE,
                            show_type=ShowType.HIGHLIGHT), ('^' + (DEVICE_TABLE_LINE_LENGTH + 11).__str__())) + '┇\n' \
                       + ('┣' + '┅' * DEVICE_TABLE_LINE_LENGTH) + '┫\n' \
                       + '┇' + format(ColorPrinter.get_color_string('Прибор', ShowType.HIGHLIGHT), '^25') \
                       + '┇' + format(ColorPrinter.get_color_string('Т обслуживания', ShowType.HIGHLIGHT), '^32') \
                       + '┇' + format(ColorPrinter.get_color_string('Кол-во заявок', ShowType.HIGHLIGHT), '^32') \
                       + '┇' + format(ColorPrinter.get_color_string('Коэф. использ.', ShowType.HIGHLIGHT), '^28') + '┇\n' \
                       + ('┣' + '┅' * DEVICE_TABLE_LINE_LENGTH) + '┫\n'
                        )

    for device in device_list:
        # 处理机 ID
        device_id = device.id

        # 处理总时长
        serve_time = device.serve_time

        # 处理过的请求数
        num_been_server_request = device.num_been_request

        # 使用率
        usage_rate = device.serve_time / timeline.get_time()

        str_device_table += (
          '┇' + format(ColorPrinter.get_color_string('П' + device_id.__str__(), ShowType.HIGHLIGHT), '^25') \
          + '┇' + format(ColorPrinter.get_color_string(serve_time.__str__()), '^22') \
          + '┇' + format(ColorPrinter.get_color_string(num_been_server_request.__str__()), '^22') \
          + '┇' + format(ColorPrinter.get_color_string((round(usage_rate, 5)).__str__()), '^18') + '┇\n' \
          + ('┣' + '┅' * DEVICE_TABLE_LINE_LENGTH) + '┫\n'
            )

    return str_device_table