# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 16:57
# @Author  : Meng Jianing
# @FileName: autoTestTool.py
# @Software: PyCharm
# @Versions: v0.1
# @Github  ：https://github.com/NekoSilverFox
# --------------------------------------------
from model.event import Event
from model.timeLine import TimeLine
from model.request import Request

if __name__ == '__main__':
    tmp = Event(1, Event.REQUEST_CREATE, 2, 3, 4, 5, 6)
    print(tmp)

    tmp = Event(1, Event.REQUEST_CREATE, 2, None, 4, 5, 6)
    print(tmp)

    i = 1
    print(i.__str__())

    r = Request(2, 1)
    print(r)
    r2 = Request(2, 3)
    print(r2)

    # print('开始测试 TimeLine')

    # while True:
    #     tl = TimeLine(0.1)
    #     print(tl.get_time())
    #     tl.time_go()
