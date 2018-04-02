from __future__ import absolute_import

import time
from pymongo import MongoClient

from .celery import app
from . import default_wallet

#client = MongoClient('database', 27018)
#db = client.mongodb_test
#collection = db.celery_test
#post = db.test


@app.task(bind=True, default_retry_delay=10)
def send_tokens(self, address, value, request_id):
    try:
        tx_hash = default_wallet.send_zeew(address, value)
    except Exception as exc:
        raise self.retry(exc=exc)
    return true

