# -*- coding: utf-8 -*-
# @Time    : 2021/11/25 20:35
# @Author  : Meng Jianing
# @FileName: request.py
# @Software: PyCharm
# @Versions: v0.1
# @Github  ：https://github.com/NekoSilverFox
# --------------------------------------------

class Request:
    """请求"""

    __num_request = 0  # 累计生成请求的数量

    def __init__(self, source, request_id):
        """初始化一个请求

        :param source: 生成这个请求的源
        :param request_id: 分配给这个请求的 ID（从 1 开始编号）
        """
        self.source = source        # 产生这个请求的源
        self.request_id_in_source = request_id        # 这个请求在它源中的ID
        Request.__num_request += 1
        self.request_id_in_cmo = Request.__num_request    # 在整个 CMO 中的唯一 ID

    def __str__(self):
        """ 返回说明当前请求(Request)的字符串

        :return: 说明当前请求(Request)的字符串
        """
        return format('\033[36;1m[Request]\033[0m Number in CMO: %s' % self.request_id_in_cmo, '<45') \
               + format('Source: %s' % self.source.id, '<20')\
               + format('Request ID in source: %s' % self.request_id_in_source, '<30')
