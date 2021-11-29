# -*- coding: utf-8 -*-
# @Time    : 2021/11/25 15:38
# @Author  : Meng Jianing
# @FileName: timeLine.py
# @Software: PyCharm
# @Versions: v0.1
# @Github  ：https://github.com/NekoSilverFox
# --------------------------------------------
from model.buffer import Buffer
from model.device import Device


class TimeLine:
    """时间线 - 手动控制时间的向后移动"""

    # 记录第一个被创建对象的引用
    __instance = None

    # 是否执行过初始化动作
    __init_flag = False

    def __init__(self, time_unit=1):
        """ 时间线的初始化，采用单例模式

        :param time_unit: 之后增加的每单位时间，默认为 1，只允许在初始化时指定
        """
        # 1.判断是否执行过初始化动作
        # 注意：用类名调用就可以
        if TimeLine.__init_flag:
            return

        # 如果没有初始化
        print("\033[33;1m[INFO]\033[0m Init time line")

        TimeLine.__init_flag = True
        self.__time_now = 0  # 模拟时间
        self.__time_unit = time_unit  # __time_unit 时间的步长（每单位时间是多久）默认为 1
        self.__debug_mode = False  # 调试（单步）模式，如果为 True 每次发生事件时等待用户按键
        self.__print_event = True  # 事件发生时是否输出
        self.log = []  # 日志，记录时间（Event）

    def __new__(cls, *args, **kwargs):
        # 1. 判断类属性是否为空对象
        if cls.__instance is None:

            # 2. 调用父类的方法，为第一个对象分配空间
            cls.__instance = super().__new__(cls)  # 【重点】为对象分配空间

            # 创建对象时，new方法会自动被调用
            print("\033[33;1m[INFO]\033[0m Create time line")

        # 3. 返回对象的引用
        return cls.__instance

    def __str__(self):
        """ 返回说明当前时间的字符串

        :return: 说明当前时间的字符串
        """
        return "Now time is " + self.__time_now.__str__()

    def reset(self):
        """ 将时间归零，事件列表清空

        :return: 无
        """
        self.__time_now = 0
        self.log.clear()

    def get_time(self):
        """ 获取当前时间

        :return: 当前时间
        """
        return self.__time_now

    def get_time_unit(self):
        """ 获取每单位时间的时长，在初始化时间线（TimeLine）时指定
            **后续的时间增长单位建议使用本方法获取，避免事件发生异常**

        :return: 每单位时间
        """
        return self.__time_unit

    def time_go(self):
        """ 向后增加一单位的时间，每单位时间在初始化时指定

        :return: True
        """
        self.__time_now += self.__time_unit
        return True

    def add_event(self, event):
        """ 将事件添加至日志

        :param event: 事件
        :return: 成功则返回 True，失败返回 False
        """
        if event is None:
            return False

        self.log.append(event)
        # print(event)

        if self.__print_event:
            print(event.__str__() \
                  + format('Num vacant buffer: %s' % Buffer.num_vacant_buffer.__str__(), "<25") \
                  + format('Num vacant device: %s' % Device.num_vacant_device.__str__())
                  )

        # 【拦截事件】
        # 如果当前模式为Debug（单步）模式，等待用户按键
        # - 如果用户按下回车，则继续运行，直至下一个时间
        # - 如果用户按下 ESC 键，关闭 Debug 模式，程序运行至结束
        if self.__debug_mode:
            key = input('>>> Press Enter to continue, `q` to exit debug mode...')
            if key == 'q' or key == 'Q':
                self.debug_off()
                print('[INFO] Stop debug mode, programmer continue')

        return True

    def debug_on(self):
        """ 启用 debug 调试（单步）模式

        :return: 无
        """
        self.__debug_mode = True

    def debug_off(self):
        """ 停用 debug 调试（单步）模式

        :return: 无
        """
        self.__debug_mode = False

    def is_debug(self):
        """ 是否开启了 debug 调试（单步）模式

        :return: 开启了 debug 调试（单步）模式返回 True，否则返回 False
        """
        return self.__debug_mode

    def print_event_on(self):
        """当事件发生时，打印输出

        :return: 无
        """
        self.__print_event = True

    def print_event_off(self):
        """当事件发生时，不打印输出

        :return: 无
        """
        self.__print_event = False

    def is_print_event(self):
        """ 事件发生时，是否打印输出

        :return: 如果打印输出事件返回 True，否则返回 False
        """
        return self.__print_event
