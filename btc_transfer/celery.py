from __future__ import absolute_import

from celery import Celery

app = Celery('btc_transfer', broker='amqp://admin:mypass@rabbit:5672',
             backend='rpc://', include=['btc_transfer.tasks'])

app.conf.update(
                CELERY_TASK_SERIALIZER='json',
                CELERY_RESULT_SERIALIZER='json',
                CELERY_ACCEPT_CONTENT=['json'],
                CELERY_TIMEZONE='Europe/Moscow',
                CELERY_ENABLE_UTC=True,
                CELERY_TRACK_STARTED=True,
                CELERY_RESULT_PERSISTENT=True,
                )
