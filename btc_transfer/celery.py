from __future__ import absolute_import

from celery import Celery
import os

app = Celery('btc_transfer', broker='amqp://admin:mypass@rabbit:5672',
             backend='rpc://', include=['btc_transfer.tasks'])
