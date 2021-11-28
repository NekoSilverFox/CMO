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
from model.event import Event


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
        duration_lambda = round(duration_lambda, 2)  # 第二位为精度，保留两位小数

        if duration_lambda < 0 or duration_lambda > 1:
            print('[ERROR] LAMBDA should between 0 and 1')  # TODO 替换为抛出异常
            exit(1)

        # 创建并插入处理机（device）
        device = Device(timeline, duration_handle, duration_lambda)
        device_list.append(device)

        if is_print_info:
            print('\033[3;32mDevice %d created:\033[0m' % i)
            print('\t' + device.__str__() + '\n')

    # 将列表反转，即优先级大的在前面
    device_list.reverse()

    return device_list



def push_request_in_buffer_list(request, buffer_list):
    """ 向缓冲区列表 buffer_list 中选择优先级最大的 Buffer 并将请求插入，返回 True
    如果所有的缓冲区都被占用，则返回 False

    :param request: 要插入的请求
    :param buffer_list: 存储多个缓冲区的列表
    :return: 插入成功返回 True‘失败返回 False
    """
    for buffer in buffer_list:
        if buffer.request_in_buffer is None:
            buffer.push_request(request)
            return True

    return False


def choose_buffer_from_buffer_list(buffer_list):
    """从 buffer_list 中选择应该弹出请求的那个 Buffer，如果所有 Buffer 中都没有请求则返回 None
    选择规则：
        - 选择优先级最大的请求（请求的优先级就为产生这个请求 源的优先级）
        - 如果优先级相同则选择最后一个进入缓冲区的

    :param buffer_list: 存有多个缓冲区（Buffer）对象的列表
    :return: 缓冲区（Buffer）对象 或 None（如果所有缓冲区都为空）
    """

    if (buffer_list is None) or (len(buffer_list) == 0) or (Buffer.num_vacant_buffer == Buffer.num_buffer):
        print('\033[1;37;41m[WARNING]\033[0m Buffer list is empty!')  # TODO 修改或删除
        return None

    max_request_priority = -1  # 最大优先级的 Request
    last_request_with_max_priority_in_buffer = -1  # 如果请求的优先级【一样】，那么选最后一个进入 Buffer 的
    return_buffer = None  # 应从选择那个 Buffer 中的请求弹出

    for buffer in buffer_list:

        # 如果当前 Buffer 中有请求，且 Buffer 中请求的优先级【大于或等于】当前记录的
        if buffer.request_in_buffer is not None \
                and buffer.request_in_buffer.source.priority >= max_request_priority:

            # 如果 Buffer 中请求的优先级【大于】当前的优先级，直接记录并开启下次循环
            if buffer.request_in_buffer.source.priority > max_request_priority:
                max_request_priority = buffer.request_in_buffer.source.priority
                last_request_with_max_priority_in_buffer = buffer.request_push_time
                return_buffer = buffer
                continue

            # 如果 Buffer 中请求的优先级【等于】当前的优先级，就选最后一个进入 Buffer 的
            if buffer.request_in_buffer.source.priority == max_request_priority \
                    and buffer.request_push_time > last_request_with_max_priority_in_buffer:
                last_request_with_max_priority_in_buffer = buffer.request_push_time
                return_buffer = buffer

    return return_buffer


def done_request_in_device_list(device_list):
    """如果调用此方法时，处理机中的请求在当前时刻完成了处理，则从处理机中弹出请求

    :param device_list: 存有多个处理机（Device）对象的列表
    :return: 此时刻完成处理的请求数
    """
    if (device_list is None) or (len(device_list) == 0):
        return 0

    num_done_request = 0
    for device in device_list:
        request = device.pop_request()
        if request is not None:
            num_done_request += 1
            # print(request.__str__())

    return num_done_request


def get_request_cmo_id_list_by_source(timeline, source):
    """ 根据源获取有个这个源产生的所有请求的ID的列表（ID为这个请求在整个CMO系统中的ID）

    :param timeline: 时间线
    :param source: 源
    :return: 源产生的所有请求的ID的列表（ID为这个请求在整个CMO系统中的ID）
    """
    if timeline is None or source is None:
        return None

    source_id = source.id
    request_cmo_id_list = []

    for event in timeline.log:
        if event.source_id == source_id and event.event_type == Event.REQUEST_CREATE:
            request_cmo_id_list.append(event.request_id_in_cmo)

    return request_cmo_id_list


def push_request_in_device_list(request, device_list):
    """向Device列表中按照优先级插入请求

    :param request: 要插入的请求
    :param device_list: 存储处理机 Device 的列表
    :return: 插入成功返回 True，失败返回 False
    """
    if request is None or device_list is None:
        print('\033[1;37;41m[ERROR]\033[0m Device list or request is empty!')
        return False

    # 如果所有处理机都被占用，则无法插入
    if Device.num_vacant_device == 0:
        print('\033[1;37;41m[WARNING]\033[0m Do not have vacant Device, push failed!')
        return False

    for device in device_list:
        if device.request_in_device is None:
            device.push_request(request)
            return True


def get_request_wait_time_list_in_buffer_by_source(timeline, source):
    """ 根据源获取由这个源生成的请求在缓冲中等待时长的 list列表，列表的每一个项代表一个请求的等待时长。被取消的请求不纳入统计当中

    :param timeline: 来记录有时间的时间线
    :param source: 查看由哪个源产生的请求
    :return: 请求在缓冲中等待时长的 list列表
    """

    if timeline is None or source is None:
        return None

    # 在存储 wait_time_list 中，存储了保存有等待信息的【元组】：(request id in cmo, request id in source, wait time)
    wait_time_list = []

    # 先获取这个源产生请求在CMO中ID的列表
    request_cmo_id_list = get_request_cmo_id_list_by_source(timeline, source)

    # 分别获取他们的等待信息的【元组】：(request id in cmo, request id in source, wait time)（如果请求没被取消的话）
    for request_cmo_id in request_cmo_id_list:

        request_join_buffer_time = 0

        for event in timeline.log:
            # 如果不是当前需求的请求，直接跳过，进行下一次循环
            if event.request_id_in_cmo != request_cmo_id:
                continue

            # 如果该请求被取消了，就没有判断这个请求的必要了，直接进行中断当前请求的处理
            if event.event_type is Event.REQUEST_CANCEL:
                break

            # 如果事件为该请求进入缓冲区，记录进入时间
            if event.event_type is Event.REQUEST_PUSH_IN_BUFFER:
                request_join_buffer_time = event.happen_time

            # 如果事件为该请求退出缓冲区，记录退出时间，写入 wait_time_list 集合当中，并进行下一次外层循环
            if event.event_type is Event.REQUEST_POP_FROM_BUFFER:
                wait_time = event.happen_time - request_join_buffer_time
                wait_time_list.append((event.request_id_in_cmo, event.request_id_in_source, wait_time))
                break

    return wait_time_list


def get_request_handle_time_list_in_device_by_source(timeline, source):
    """ 根据源获取由这个源生成的请求在处理机中处理时长的 list列表，列表的每一个项代表一个请求的处理时长。被取消的请求不纳入统计当中

    :param timeline: 来记录有时间的时间线
    :param source: 查看由哪个源产生的请求
    :return: 请求在处理机中处理时长的 list列表
    """

    if timeline is None or source is None:
        return None

    # 在存储 wait_time_list 中，存储了保存有等待信息的【元组】：(request id in cmo, request id in source, wait time)
    handle_time_list = []

    # 先获取这个源产生请求在CMO中ID的列表
    request_cmo_id_list = get_request_cmo_id_list_by_source(timeline, source)

    # 分别获取他们的等待信息的【元组】：(request id in cmo, request id in source, handle time)（如果请求没被取消的话）
    for request_cmo_id in request_cmo_id_list:

        request_join_device_time = 0

        for event in timeline.log:
            # 如果不是当前需求的请求，直接跳过，进行下一次循环
            if event.request_id_in_cmo != request_cmo_id:
                continue

            # 如果该请求被取消了，就没有判断这个请求的必要了，直接进行中断当前请求的处理
            if event.event_type is Event.REQUEST_CANCEL:
                break

            # 如果事件为该请求进入缓冲区，记录进入时间
            if event.event_type is Event.REQUEST_PUSH_IN_DEVICE:
                request_join_device_time = event.happen_time

            # 如果事件为该请求退出缓冲区，记录退出时间，写入 wait_time_list 集合当中，并进行下一次外层循环
            if event.event_type is Event.REQUEST_POP_FROM_DEVICE:
                handle_time = event.happen_time - request_join_device_time
                handle_time_list.append((event.request_id_in_cmo, event.request_id_in_source, handle_time))
                break

    return handle_time_list


def get_request_live_time_list_in_device_by_source(timeline, source):
    """ 根据源获取由这个源生成的请求在整个CMO系统中的生命时长（从源产生到源被取消或者结束处理）的 list列表，列表的每一个项代表一个请求的处理时长。被取消的请求不纳入统计当中

    :param timeline: 来记录有时间的时间线
    :param source: 查看由哪个源产生的请求
    :return: 请求在处理机中处理时长的 list列表
    """

    if timeline is None or source is None:
        return None

    # 在存储 wait_time_list 中，存储了保存有等待信息的【元组】：(request id in cmo, request id in source, wait time)
    live_time_list = []

    # 先获取这个源产生请求在CMO中ID的列表
    request_cmo_id_list = get_request_cmo_id_list_by_source(timeline, source)

    # 分别获取他们的等待信息的【元组】：(request id in cmo, request id in source, live time)（如果请求没被取消的话）
    for request_cmo_id in request_cmo_id_list:

        request_create_time = 0

        for event in timeline.log:
            # 如果不是当前需求的请求，直接跳过，进行下一次循环
            if event.request_id_in_cmo != request_cmo_id:
                continue

            # 如果事件为该请求被创建，记录创建时间，该请求生命周期开始
            if event.event_type is Event.REQUEST_CREATE:
                request_create_time = event.happen_time

            # 如果该请求被取消或者完成处理，该请求生命周期结束
            if (event.event_type is Event.REQUEST_CANCEL) or (event.event_type is Event.REQUEST_POP_FROM_DEVICE):
                live_time = event.happen_time - request_create_time
                live_time_list.append((event.request_id_in_cmo, event.request_id_in_source, live_time))
                break

    return live_time_list


def get_request_cancel_list_in_device_by_source(timeline, source):
    """ 根据源获取由这个源生成的请求被取消的 list列表

    :param timeline: 来记录有时间的时间线
    :param source: 查看由哪个源产生的请求
    :return: 由这个源生成的请求被取消的 list列表
    """

    if timeline is None or source is None:
        return None

    # 在存储 cancel_list 中，存储了保存有等待信息的【元组】：(request id in cmo, request id in source, cancel time)
    cancel_list = []

    # 先获取这个源产生请求在CMO中ID的列表
    request_cmo_id_list = get_request_cmo_id_list_by_source(timeline, source)

    # 分别获取他们的取消信息的【元组】：(request id in cmo, request id in source, cancel time)
    for request_cmo_id in request_cmo_id_list:

        for event in timeline.log:
            # 如果不是当前需求的请求，直接跳过，进行下一次循环
            if event.request_id_in_cmo != request_cmo_id:
                continue

            # 如果该请求被取消，添加记录
            if event.event_type is Event.REQUEST_CANCEL:
                cancel_list.append((event.request_id_in_cmo, event.request_id_in_source, event.happen_time))
                break

    return cancel_list







