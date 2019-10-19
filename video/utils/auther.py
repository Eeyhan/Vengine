#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : Eeyhan
# @File    : auther.py

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from app1 import models
from django.utils.timezone import now
import requests
import geoip2.database

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,application/json, text/javascript,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64;Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'close',
    'Accept-Encoding': 'gzip, deflate',
    'Upgrade-Insecure-Requests': '1'
}
CHECK_URL = 'http://ip.taobao.com/service/getIpInfo.php?ip={ip}'


class MyAuth(BaseAuthentication):
    """认证"""

    def authenticate(self, request):
        # 验证请求头
        headers = request.META.get('HTTP_USER_AGENT')
        client_header = {'python', 'php', 'java', 'go', 'c#', 'c++'}
        for h in client_header:
            if h in headers.lower():
                raise AuthenticationFailed('身份识别不通过')
        # 验证ip
        # client_ip = request.META.get('REMOTE_ADDR') # 真实项目使用
        client_ip = '183.14.135.241'  # 测试使用
        if ',' in client_ip:  # 使用了代理
            raise AuthenticationFailed('非法访问')
        elif ':' in client_ip:  # 使用了代理
            raise AuthenticationFailed('非法访问')
        else:
            # 调取geoip库
            reader = geoip2.database.Reader('./utils/GeoLite2-Country.mmdb')
            response = reader.country(client_ip)
            data = response.country.iso_code
            if not data:
                # ip不在geoip数据库内，原则上不采取这个方法，增加IO阻塞
                url = CHECK_URL.format(ip=client_ip)
                res = requests.get(url, headers=HEADERS)
                country_data = res.json()['data']
                c = country_data.get('country')
                if c and '中国' in c:
                    request_obj = models.RequestInfo.objects.filter(ip=client_ip).first()
                    if not request_obj:
                        request_obj = models.RequestInfo.objects.create(last_time=now(), ip=client_ip)
                    return request_obj, ''
                else:
                    raise AuthenticationFailed('非法访问')
            elif data == 'CN':
                # 验证通过
                request_obj = models.RequestInfo.objects.filter(ip=client_ip).first()
                if not request_obj:
                    request_obj = models.RequestInfo.objects.create(last_time=now(), ip=client_ip)
                return request_obj, ''
            else:
                raise AuthenticationFailed('非法访问')
