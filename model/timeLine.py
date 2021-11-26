# -*- coding: utf-8 -*-
# @Time    : 2021/11/25 15:38
# @Author  : Meng Jianing
# @FileName: timeLine.py
# @Software: PyCharm
# @Versions: v0.1
# @Github  ：https://github.com/NekoSilverFox
# --------------------------------------------

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
        print("[INFO] Init time line")

        # 模拟时间
        self.__time_now = 0
        self.__time_unit = time_unit  # __time_unit 时间的步长（每单位时间是多久）默认为 1
        TimeLine.__init_flag = True
        self.log = []  # 日志，记录时间（Event）

    def __new__(cls, *args, **kwargs):
        # 1. 判断类属性是否为空对象
        if cls.__instance is None:

            # 2. 调用父类的方法，为第一个对象分配空间
            cls.__instance = super().__new__(cls)  # 【重点】为对象分配空间

            # 创建对象时，new方法会自动被调用
            print("[INFO] Create time line")

        # 3. 返回对象的引用
        return cls.__instance

    def __str__(self):
        """ 返回说明当前时间的字符串

        :return: 说明当前时间的字符串
        """
        return "Now time is " + self.__time_now.__str__()

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

        :return: None
        """
        self.__time_now += self.__time_unit

    def add_event(self, event):
        """ 将事件添加至日志

        :param event: 事件
        :return: 成功则返回 True，失败返回 False
        """
        if event is None:
            return False

        self.log.append(event)
        return True
