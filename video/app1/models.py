from django.db import models


# Create your models here.


class VideoInfo(models.Model):
    """影视表"""
    title = models.CharField(max_length=32, verbose_name='名称')
    status = models.CharField(max_length=10, verbose_name='状态', null=True, blank=True)
    property = models.CharField(max_length=10, verbose_name='属性', null=True, blank=True)
    types = models.CharField(max_length=10, verbose_name='类型', null=True, blank=True)
    area = models.CharField(max_length=10, verbose_name='国区', null=True, blank=True)
    lang = models.CharField(max_length=5, verbose_name='语言', null=True, blank=True)
    grade = models.FloatField(max_length=3, verbose_name='评分', null=True, blank=True)
    director = models.CharField(max_length=10, verbose_name='导演', null=True, blank=True)
    actors = models.CharField(max_length=128, verbose_name='主演', null=True, blank=True)
    # update_time = models.DateTimeField(verbose_name='更新时间', null=True, blank=True)
    # 存入的时间格式不统一，所以直接用字符串格式
    update_time = models.CharField(max_length=64, verbose_name='更新时间', null=True, blank=True)
    show_time = models.IntegerField(verbose_name='上映年份', null=True, blank=True)
    info = models.CharField(max_length=256, verbose_name='简介', null=True, blank=True)
    m3u8_link = models.CharField(max_length=5120000, verbose_name='m3u8地址', null=True, blank=True)
    online_link = models.CharField(max_length=5120000, verbose_name='在线播放地址', null=True, blank=True)
    xunlei_link = models.CharField(max_length=5120000, verbose_name='迅雷下载地址', null=True, blank=True)

    class Meta:
        verbose_name = '影视表'
        verbose_name_plural = 'DB_VideoInfo'
        db_table = verbose_name_plural

    def __str__(self):
        return self.title
