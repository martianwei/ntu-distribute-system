from celery import Celery
from configs import configs
from kombu import Queue, Exchange

celery_app = Celery(configs.APP_NAME,
                    include=['reservation_app.tasks'])

QUEUE_NAME = 'movie_reservation_queue'

queue = (
    Queue(name=QUEUE_NAME, exchange=Exchange(
        'default', type='direct')),
)


celery_app.conf.update(
    task_queues=queue,
    timezone='Asia/Taipei',  # 设置时区
    enable_utc=False,  # 默认为true，UTC时区
    broker_url=configs.CELERY_BROKER_URL,  # broker，注意rabbitMQ的VHOST要给你使用的用户加权限
    result_backend=configs.CELERY_RESULT_BACKEND,  # backend配置，注意指定redis数据库
    worker_concurrency=4,  # worker最大并发数
    worker_max_tasks_per_child=100,  # 每个worker最多执行100个任务被销毁，可以防止内存泄漏
    task_acks_late=True,  # 如果不设置，默认是celery队列，此处使用默认的直连交换机，routing_key完全一致才会调度到celery_demo队列
    worker_prefetch_multiplier=1,
    result_expires=3600,  # 任务结果过期时间
)
