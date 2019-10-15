#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : Eeyhan
# @File    : serializers.py

from rest_framework import serializers
from app1 import models


class VideoSerializer(serializers.ModelSerializer):
    """影视表"""

    class Meta:
        model = models.VideoInfo
        fields = '__all__'
