# -*- coding: utf-8 -*-
# @Time    : 2021/11/25 20:35
# @Author  : Meng Jianing
# @FileName: request.py
# @Software: PyCharm
# @Versions: v0.1
# @Github  ：https://github.com/NekoSilverFox
# --------------------------------------------

class Request:

    __num_request = 0  # 累计生成请求的数量

    def __init__(self, source, request_id):
        """初始化一个请求

        :param source: 生成这个请求的源
        :param request_id: 分配给这个请求的 ID
        """
        self.source = source
        self.id = request_id
        Request.__num_request += 1
        self.num_request = Request.__num_request

    def __str__(self):
        return format('[Request] Number in CMO: %s' % self.__num_request, '<35') \
               + format('Source: %s' % self.source, '<20')\
               + format('Request ID in source: %s' % self.id, '<30')
