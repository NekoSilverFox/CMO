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

if __name__ == '__main__':
    tmp = Event(1, Event.REQUEST_CREATE, 2, 3, 4, 5, 6)
    print(tmp)

    tmp = Event(1, Event.REQUEST_CREATE, 2, None, 4, 5, 6)
    print(tmp)

    tl = TimeLine()
    TimeLine()
    TimeLine()

    i = 1
    print(i.__str__())

