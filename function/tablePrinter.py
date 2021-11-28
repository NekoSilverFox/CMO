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
DEVICE_TABLE_LINE_LENGTH = 150


def source_info_table_cn(timeline, source_list):
    # 如果程序正确，那么 请求停留总时间 = 缓冲中等待时间 + 服务时间
    str_source_table = ('┏' + '┅' * DEVICE_TABLE_LINE_LENGTH) + '┓\n'\
                       + '┇' + format(ColorPrinter.get_color_string(
                            string='Source info table',
                            fore_color=ForeColor.GREEN,
                            show_type=ShowType.HIGHLIGHT), ('^' + (DEVICE_TABLE_LINE_LENGTH + 11).__str__())) + '┇\n'\
                       + ('┣' + '┅' * DEVICE_TABLE_LINE_LENGTH) + '┫\n'\
                       + '┇' + format(ColorPrinter.get_color_string('Source', ShowType.HIGHLIGHT), '^21')\
                       + '┇' + format(ColorPrinter.get_color_string('生成的请求数', ShowType.HIGHLIGHT), '^21')\
                       + '┇' + format(ColorPrinter.get_color_string('请求的取消率', ShowType.HIGHLIGHT), '^23')\
                       + '┇' + format(ColorPrinter.get_color_string('请求停留总时间', ShowType.HIGHLIGHT), '^24')\
                       + '┇' + format(ColorPrinter.get_color_string('缓冲中等待时间', ShowType.HIGHLIGHT), '^24')\
                       + '┇' + format(ColorPrinter.get_color_string('服务时间', ShowType.HIGHLIGHT), '^24')\
                       + '┇' + format(ColorPrinter.get_color_string('等待时间的方差', ShowType.HIGHLIGHT), '^23')\
                       + '┇' + format(ColorPrinter.get_color_string('服务时间的方差', ShowType.HIGHLIGHT), '^23') + '┇\n' \
                       + ('┣' + '┅' * DEVICE_TABLE_LINE_LENGTH) + '┫\n' \

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
        ave_wait_time = all_request_wait_time_in_buffer / (num_request - num_cancel_request)  # 在 Buffer 中的平均等待时长
        for event_wait_time in live_wait_time_list:
            variance_wait_time += ((event_wait_time[2] - ave_wait_time) ** 2)
        variance_wait_time /= (num_request - num_cancel_request)

        # 计算这个源生成请求在 Device 中的处理时长的【方差】
        ave_handle_time = all_request_handle_time / (num_request - num_cancel_request)  # 在 Device 中的平均等待时长
        for event_handle_time in live_handle_time_list:
            variance_handle_time += ((event_handle_time[2] - ave_handle_time) ** 2)
        variance_handle_time /= (num_request - num_cancel_request)

        str_source_table += (
          '┇' + format(ColorPrinter.get_color_string('И' + source_id.__str__(), ShowType.HIGHLIGHT), '^21') \
        + '┇' + format(ColorPrinter.get_color_string(num_request.__str__()), '^17') \
        + '┇' + format(ColorPrinter.get_color_string((round((probability_cancel * 100), 5).__str__() + ' %')), '^18') \
        + '┇' + format(ColorPrinter.get_color_string(all_request_live_time.__str__()), '^20') \
        + '┇' + format(ColorPrinter.get_color_string(all_request_wait_time_in_buffer.__str__()), '^20') \
        + '┇' + format(ColorPrinter.get_color_string(all_request_handle_time.__str__()), '^18') \
        + '┇' + format(ColorPrinter.get_color_string((round(variance_wait_time, 5)).__str__()), '^20') \
        + '┇' + format(ColorPrinter.get_color_string((round(variance_handle_time, 5)).__str__()), '^19') + '┇\n' \
        + ('┣' + '┅' * DEVICE_TABLE_LINE_LENGTH) + '┫\n'
            )

    return str_source_table
