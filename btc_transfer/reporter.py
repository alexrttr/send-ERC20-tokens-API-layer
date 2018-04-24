from jsonrpcclient.http_client import HTTPClient
from jsonrpcclient.request import Request
import logging
import os

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

inv_host = os.environ.get('INVESTMENT_HOST', '192.168.0.45')
inv_port = os.environ.get('INVESTMENT_RPC_PORT', '7081')

client = HTTPClient(f'http://{inv_host}:{inv_port}')


def report(req, tx, status):
    logging.debug(f'sending report for {req}')
    request = Request(f'reportStatus', req, status, tx)
    client.notify(request)
