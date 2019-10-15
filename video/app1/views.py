from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.tools import BaseResponse
from app1.serializers import VideoSerializer
from app1.models import VideoInfo
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
import redis
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

# Create your views here.


scheduler = BackgroundScheduler()  # 创建一个调度器对象
scheduler.add_jobstore(DjangoJobStore(), "default")  # 添加一个作业

try:
    # @register_job(scheduler, "interval", seconds=60, max_instances=2)  # 每1秒执行一次
    @register_job(scheduler, 'cron', day_of_week='mon-sun', hour='01', minute='30',
                  second='00')  # 定时执行：这里定时为周一到周日每天早上01：30执行一次
    def time_task():
        """定时的任务逻辑:你要定时执行的任务"""
        async_search_func()


    register_events(scheduler)
    scheduler.start()
    # scheduler.remove_job(time_task)  # 移除定时任务
except Exception as e:
    print(e)
    scheduler.shutdown()


def async_search_func():
    """多个任务爬取"""
    conn = redis.Redis(connection_pool=settings.POOL)
    search_args = conn.smembers('search_args')
    # 检测是否已有值
    if search_args:
        for args in search_args:

            """爬取部分，自行补充"""
            result = ''

            # 存入mysql
            if result:
                result_objs = []
                for item in result:
                    v_obj = VideoInfo(title=item['m_title'], status=item['m_status'], property=item['m_property'],
                                      types=item['m_type'], area=item['m_area'], lang=item['lang'],
                                      director=item['director'], grade=item['m_grade'], actors=item['actors'],
                                      update_time=item['m_update_time'], show_time=item['show_time'], info=item['info'],
                                      m3u8_link=item['m3u8_link'], online_link=item['online_link'],
                                      xunlei_link=item['xunlei_link'],
                                      )
                    result_objs.append(v_obj)
                VideoInfo.objects.bulk_create(result_objs)
                conn.srem('search_args', args)


def save_orm(data):
    if data:
        result_objs = []
        for item in data:
            v_obj = VideoInfo(title=item['m_title'], status=item['m_status'], property=item['m_property'],
                              types=item['m_type'], area=item['m_area'], lang=item['lang'],
                              director=item['director'], grade=item['m_grade'], actors=item['actors'],
                              update_time=item['m_update_time'], show_time=item['show_time'], info=item['info'],
                              m3u8_link=item['m3u8_link'], online_link=item['online_link'],
                              xunlei_link=item['xunlei_link'],
                              )
            result_objs.append(v_obj)
        VideoInfo.objects.bulk_create(result_objs)


def save_redis(key):
    """将暂无搜索记录的数据存入redis"""
    conn = redis.Redis(connection_pool=settings.POOL)
    if key:
        conn.sadd('search_args', key)


def index(request):
    return render(request, 'index.html')


class VideoView(APIView):
    """影视类"""

    def get(self, request):
        return Response('test')

    def post(self, request):
        res = BaseResponse()
        name = request.data.get('name')
        if name:
            all_obj = VideoInfo.objects.filter(title__contains=name).all().extra(
                select={'_has1': 'instr(title, "花絮")'}).extra(
                select={'_has2': 'instr(title, "记录")'}).order_by('_has1', '_has2')
            if all_obj:
                serializer_obj = VideoSerializer(all_obj, many=True)
                res.data = serializer_obj.data
                res.code = 200
                return Response(res.dict)
            else:
                # 记录搜索词汇，设定时间周期爬取
                res.data = '您搜索的影视词汇 “%s” 目前暂无数据，请明天再来搜索，数据24小时定期更新' % name
                res.code = 202
                save_redis(name)
                return Response(res.dict)
