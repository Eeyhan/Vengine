#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : Eeyhan
# @File    : BaseReponse.py


class BaseResponse(object):
    def __init__(self):
        self.code = None
        self.data = None
        self.error = None

    @property
    def dict(self):
        return self.__dict__

