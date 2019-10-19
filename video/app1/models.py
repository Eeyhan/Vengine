from django.db import models


# Create your models here.


class VideoInfo(models.Model):
    """影视表"""
    title = models.CharField(max_length=32, verbose_name='名称', unique=True)
    status = models.CharField(max_length=10, verbose_name='状态', null=True, blank=True)
    property = models.CharField(max_length=10, verbose_name='属性', null=True, blank=True)
    types = models.CharField(max_length=10, verbose_name='类型', null=True, blank=True)
    area = models.CharField(max_length=10, verbose_name='国区', null=True, blank=True)
    lang = models.CharField(max_length=20, verbose_name='语言', null=True, blank=True)
    grade = models.FloatField(verbose_name='评分', null=True, blank=True)
    director = models.CharField(max_length=64, verbose_name='导演', null=True, blank=True)
    actors = models.CharField(max_length=128, verbose_name='主演', null=True, blank=True)
    # update_time = models.DateTimeField(verbose_name='更新时间', null=True, blank=True)
    # 存入的时间格式不统一，所以直接用字符串格式
    update_time = models.CharField(max_length=64, verbose_name='更新时间', null=True, blank=True)
    show_time = models.IntegerField(verbose_name='上映年份', null=True, blank=True)
    info = models.CharField(max_length=256, verbose_name='简介', null=True, blank=True)
    m3u8_link = models.TextField(verbose_name='m3u8地址', null=True, blank=True)
    online_link = models.TextField(verbose_name='在线播放地址', null=True, blank=True)
    xunlei_link = models.TextField(verbose_name='迅雷下载地址', null=True, blank=True)

    class Meta:
        verbose_name = '影视表'
        verbose_name_plural = 'DB_VideoInfo'
        db_table = verbose_name_plural

    def __str__(self):
        return self.title


# class Account(models.Model):
#     """用户"""
#     username = models.CharField(verbose_name='用户名', max_length=32)
#     LEVEL_CHOICES = ((0, '匿名'), (1, '默认'), (2, '会员'))
#     level = models.IntegerField(choices=LEVEL_CHOICES, default=0, verbose_name='用户等级')
#
#     class Meta:
#         verbose_name = '用户表'
#         verbose_name_plural = 'DB_Account'
#         db_table = verbose_name_plural
#
#     def __str__(self):
#         return self.username


class RequestInfo(models.Model):
    """请求表"""
    ip = models.GenericIPAddressField(verbose_name='请求ip', unique=True)
    last_time = models.DateTimeField(verbose_name='最近一次访问时间')
    excess_times = models.IntegerField(verbose_name='过量访问次数', default=0)
    is_ban = models.BooleanField(verbose_name='是否已屏蔽', default=0)
    ban_date = models.IntegerField(verbose_name='屏蔽时间', default=3600, help_text='单位秒，默认屏蔽两小时')
    day_search_times = models.IntegerField(verbose_name='每个ip每天最多访问15次', default=15, help_text='访问的时候才创建，创建的时候算一次')

    # accounts = models.ForeignKey(to='Account', on_delete=models.CASCADE, verbose_name='关联用户')

    class Meta:
        verbose_name = '请求表'
        verbose_name_plural = 'DB_RequestInfo'
        db_table = verbose_name_plural

    def __str__(self):
        return self.ip
