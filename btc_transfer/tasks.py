from __future__ import absolute_import

import logging
from typing import NamedTuple
import traceback

from .celery import app
from .wallet import EthWallet
from .db import Redis

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
logging.info('import tasks')


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
        return f'<Report, req={self.req}, status={self.status}>'


@app.task(name='send_tokens', bind=True)
def send_tokens(self, address, value, request_id):
    try:
        tx_hash = default_wallet.send_zeew(address, value)
    except Exception:
        logging.error(f'Caught an error in send_tokens {traceback.print_exc()}')
        tx_hash = -1

    return Sent(request_id, tx_hash)


@app.task(name='add_address_to_whitelist', bind=True)
def add_wl(self, address, request_id):
    try:
        tx_hash = default_wallet.add_to_wl(address)
    except Exception:
        logging.error(f'Caught an error in add_wl {traceback.print_exc()}')
        tx_hash = -1

    return Sent(request_id, tx_hash)


@app.task(name='get_tx_status')
def get_status(serilised_send_results) -> Report:
    send_results = Sent(*serilised_send_results)
    logging.debug(f'send_tokens/add_wl_result is {send_results}')
    logging.debug(f'Celery time zone is {app.conf.timezone}')

    try:
        if send_results.tx != -1:
            status = default_wallet.get_tx_status(send_results.tx)
        else:
            status = False
    except Exception:
        logging.error(f'Caught an error in get_status {traceback.print_exc()}')
        status = False
    report = Report(send_results.req, send_results.tx, status)
    logging.debug(f'report is {report}')
    return report


@app.task(name='save_tx_results')
def save_tx_status(serilised_report):
    report = Report(*serilised_report)
    try:
        db.save_job_results(report.req, (report.tx, report.status))
    except Exception:
        logging.error(f'Caught an error in save_tx {traceback.print_exc()}')
    return report


@app.task(name='send_results_to_remote')
def send_report(report):
    from . import reporter
    reporter.report(*report)
