# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 16:57
# @Author  : Meng Jianing
# @FileName: testTool.py
# @Software: PyCharm
# @Versions: v0.1
# @Github  ：https://github.com/NekoSilverFox
# --------------------------------------------
import random

from model.source import Source
from model.buffer import Buffer
from model.device import Device


def create_source_list(timeline, num_source, min_interval, max_interval, is_print_info=True):
    """ 创建一个源（Source）的列表

    :param timeline: 时间线
    :param num_source: 要创建源的数量
    :param min_interval: 最小的时间间隔
    :param max_interval: 最大的时间间隔
    :param is_print_info: 是否在创建时打印信息
    :return: 源的列表
    """
    source_list = []

    i = 0
    while i < num_source:
        i += 1
        # 使用随机数确定时间间隔
        interval = random.randint(min_interval, max_interval)

        # 创建并插入源
        source = Source(timeline, interval)
        source_list.append(source)

        if is_print_info:
            print('\033[3;32mSource %d created:\033[0m' % i)
            print('\t' + source.__str__() + '\n')

    # 将列表反转，即优先级大的在前面
    source_list.reverse()

    return source_list


def create_buffer_list(timeline, num_buffer, is_print_info=True):
    """创建一个缓冲区（Buffer）的列表

    :param timeline: 时间线
    :param num_buffer: 要创建的缓冲区的数量
    :param is_print_info: 是否在创建时打印信息
    :return: 处理机（Buffer）的列表
    """
    buffer_list = []

    i = 0
    while i < num_buffer:
        i += 1

        # 创建并插入缓冲区
        buffer = Buffer(timeline)
        buffer_list.append(buffer)

        if is_print_info:
            print('\033[3;32mBuffer %d created:\033[0m' % i)
            print('\t' + buffer.__str__() + '\n')

    # 将列表反转，让优先级大的在前面
    buffer_list.reverse()

    return buffer_list


def create_device_list(timeline, num_device, min_duration_handle, max_duration_handle,
                       min_duration_lambda, max_duration_lambda, is_print_info=True):
    """创建一个处理机（Device）的列表

    :param timeline: 时间线
    :param num_device:  要创建的处理机的数量
    :param min_duration_handle: **最大的处理时间**，即第一个请求所需的时间（*$MaxTime > 0$*）
    :param max_duration_handle: **最小的处理时间**，即第一个请求所需的时间（*$MaxTime > 0$*）
    :param min_duration_lambda: 最小指数 - `LAMBDA` - 参数，越接近 1，函数递减的就越快（$0 < LAMBDA < 1$）
    :param max_duration_lambda: 最大指数 - `LAMBDA` - 参数，越接近 1，函数递减的就越快（$0 < LAMBDA < 1$）
    :param is_print_info: 是否在创建时打印信息
    :return: 处理机（Device）的列表
    """

    device_list = []

    i = 0
    while i < num_device:
        i += 1
        # 使用随机数确定处理请求所需的时间间隔
        duration_handle = random.randint(min_duration_handle, max_duration_handle)

        # 使用随机数确定 `LAMBDA` - 参数，越接近 1，函数递减的就越快（$0 < LAMBDA < 1$）
        duration_lambda = random.uniform(min_duration_lambda, max_duration_lambda)
        duration_lambda = round(duration_handle, 2)  # 第二位为精度，保留两位小数

        # 创建并插入处理机（device）
        device = Device(timeline, duration_handle, duration_lambda)
        device_list.append(device)

        if is_print_info:
            print('\033[3;32mDevice %d created:\033[0m' % i)
            print('\t' + device.__str__() + '\n')

    # 将列表反转，即优先级大的在前面
    device_list.reverse()

    return device_list


