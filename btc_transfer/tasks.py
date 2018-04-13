from __future__ import absolute_import

import os
import logging
from typing import NamedTuple

from .celery import app
from .wallet import EthWallet
from .db import Redis

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

DEF_ZEEW_TX_MINING_TIME = 10
mining_time = os.environ.get('ZEEW_TX_MINING_TIME', DEF_ZEEW_TX_MINING_TIME)

default_wallet = EthWallet()
db = Redis()


class Sent(NamedTuple):
    req: str
    tx: str

    def __repr__(self) -> str:
        return f'<Sent, req={self.req}, tx={self.tx}>'


class Report(NamedTuple):
    req: str
    tx: str
    status: bool

    def __repr__(self) -> str:
        return f'<Report, req={self.sent.req}, status={self.status}>'


@app.task(name='send_tokens', bind=True)
def send_tokens(self, address, value, request_id):
    return Sent(request_id, '254535')
    tx_hash = default_wallet.send_zeew(address, value)
    return Sent(request_id, tx_hash)


@app.task(name='get_tx_status', countdown=60*int(mining_time))
def get_status(serilised_send_results) -> Report:
    send_results = Sent(*serilised_send_results)
    logging.debug('send_tokens_result is {}'.format(send_results))
    logging.debug(f'Celery time zone is {app.conf.timezone}')
    return Report(send_results.req, send_results.tx, True)

    status = default_wallet.get_tx_status(send_results.tx)
    report = Report(send_results.req, send_results.tx, status)
    logging.debug(f'report is {report}')
    return report


@app.task(name='save_tx_results')
def save_tx_status(serilised_report):
    report = Report(*serilised_report)
    db.save_job_results(report.req, (report.tx, report.status))
    return report


@app.task(name='send_results_to_remote')
def send_report(report):
    import reporter

    reporter.report(*report)
