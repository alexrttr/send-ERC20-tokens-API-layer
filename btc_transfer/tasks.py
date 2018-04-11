from __future__ import absolute_import

from collections import namedtuple
import logging
import os

from .celery import app
from .wallet import EthWallet
from .db import Redis

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

DEF_ZEEW_TX_MINING_TIME = 10
mining_time = os.environ.get('ZEEW_TX_MINING_TIME', DEF_ZEEW_TX_MINING_TIME)

default_wallet = EthWallet()
db = Redis()

Sent = namedtuple('Sent', 'req tx')
Report = namedtuple('Report', 'sent status')


@app.task(name='send_tokens_task', bind=True)
def send_tokens(self, address, value, request_id):
    tx_hash = default_wallet.send_zeew(address, value)
    return Sent(request_id, tx_hash)


@app.task(name='gather_tx_results', countdown=60*mining_time)
def get_status(send_results):
    logging.debug('send_tokens_result is {}'.format(send_results))
    status = default_wallet.get_status(send_results.tx)
    report = Report(send_results, status)
    logging.debug('report is {}'.format(report))
    return report


@app.task(name='save_tx_results')
def save_tx_status(report):
    db.save_job_results(*(report.sent + (report.status,)))
    return report


@app.tesk(name='send results to remote')
def send_report(report):
    pass
