#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : Eeyhan
# @File    : throttles.py

from rest_framework.throttling import BaseThrottle
from django.utils.timezone import now
from app1 import models
from datetime import datetime, timedelta


class MyThrottle(BaseThrottle):
    def __init__(self):
        self.now = None
        self.request_obj = None

    def allow_request(self, request, view):

        # 以IP作为限流
        # ip = request.META.get('REMOTE_ADDR')  # 真实项目使用
        ip = '183.14.135.241'  # 测试使用
        request_obj = request.user
        if not request_obj:
            request_obj = models.RequestInfo.objects.filter(ip=ip).first()
        # 初始用户第一次访问
        this_now = now()
        self.now = this_now

        # 非初始用户（对应ip）当天第一次访问，重设为默认次数
        if this_now.day != request_obj.last_time.day:
            request_obj.day_search_times = 15
            request_obj.excess_times = 0
            request_obj.is_ban = 0

        # 非初始用户（对应ip）当天非第一次访问

        self.request_obj = request_obj

        # 已超过当日最大次数
        if request_obj.day_search_times <= 0:
            request_obj.save()
            return False

        # 未超过次数
        request_obj.day_search_times -= 1
        if request_obj.day_search_times < 0:
            request_obj.day_search_times = 0

        # 检测是否已屏蔽
        if request_obj.is_ban:
            # request_obj.last_time = this_now  # 已经ban的不记录上次登录时间
            # 检测是否已到解除屏蔽时间
            last_time = request_obj.last_time
            ban_date = request_obj.ban_date
            ban_date = timedelta(seconds=ban_date)
            times = (last_time + ban_date) - self.now
            if times.days >= 0:
                if times.seconds == 0:  # 刚刚好
                    request_obj.excess_times = 0
                    request_obj.is_ban = 0
                    request_obj.save()
                    return True
            else:
                request_obj.excess_times = 0
                request_obj.is_ban = 0
                request_obj.save()
                return True
            return False

        # 未屏蔽，记录登录时间
        last_time = request_obj.last_time
        this_now_stamp = datetime.timestamp(this_now)
        last_time_stamp = datetime.timestamp(last_time)
        if this_now_stamp - last_time_stamp <= 1.5:  # 1秒内请求是否超过两次
            request_obj.last_time = this_now
            request_obj.excess_times += 1  # 更新过频次数
            request_obj.save()
            return True

        # 过频访问
        if request_obj.excess_times < 5:  # 检测过频是否超过5次
            request_obj.last_time = this_now
            request_obj.save()
            return True

        # 已超过5次，ban掉，不用更新上次访问时间，直接这个时间作为ban的基数作计算
        request_obj.is_ban = True
        request_obj.save()
        return False

    def wait(self):
        # 返回需要等待的时间
        last_time = self.request_obj.last_time
        ban_date = self.request_obj.ban_date
        ban_date = timedelta(seconds=ban_date)
        end_times = (last_time + ban_date) - self.now
        return end_times.seconds
