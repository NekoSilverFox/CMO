# -*- coding: utf-8 -*-
# @Time    : 2021/11/28 0:06
# @Author  : Meng Jianing
# @FileName: tablePrinter.py
# @Software: PyCharm
# @Versions: v0.1
# @Github  ：https://github.com/NekoSilverFox
# --------------------------------------------

from colorPrinter.colorPrinter import *
DEVICE_TABLE_LINE_LENGTH = 150


def source_info_table_cn(source_list):
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
        source_id = source.id
        num_request = source.num_request
        num_cancel = None
        request_live_time = None
        request_wait_time_in_buffer = None
        work_time = None
        fc_wait = None
        fc_work = None

        str_source_table += (
                  '┇' + format(ColorPrinter.get_color_string('И' + source_id.__str__(), ShowType.HIGHLIGHT), '^21') \
                + '┇' + format(ColorPrinter.get_color_string(num_request.__str__()), '^17') \
                + '┇' + format(ColorPrinter.get_color_string(num_cancel.__str__()), '^18') \
                + '┇' + format(ColorPrinter.get_color_string(request_live_time.__str__()), '^20') \
                + '┇' + format(ColorPrinter.get_color_string(request_wait_time_in_buffer.__str__()), '^20') \
                + '┇' + format(ColorPrinter.get_color_string(work_time.__str__()), '^18') \
                + '┇' + format(ColorPrinter.get_color_string(fc_wait.__str__()), '^20') \
                + '┇' + format(ColorPrinter.get_color_string(fc_work.__str__()), '^19') + '┇\n' \
                + ('┣' + '┅' * DEVICE_TABLE_LINE_LENGTH) + '┫\n'
            )

    return str_source_table
