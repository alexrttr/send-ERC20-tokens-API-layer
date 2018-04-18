from __future__ import absolute_import

import logging
import os
import re
import signal
from twisted.web import server
from twisted.internet import reactor
from txjsonrpc.web import jsonrpc

from .celery import app
from . import tasks

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

DEF_ZEEW_TX_MINING_TIME = 10
mining_time = os.environ.get('ZEEW_TX_MINING_TIME', DEF_ZEEW_TX_MINING_TIME)

def handle_pdb(sig, frame):
    import pdb
    pdb.Pdb().set_trace(frame)


class SendTokensServer(jsonrpc.JSONRPC):
    def __init__(self):
        self.eth_address = re.compile('^(0x)?[0-9a-fA-F]{40}$')
        self.rpc_port = os.environ.get('RPC_PORT', 7080)

    def _address_valid(self, address):
        return re.match(self.eth_address, address)

    def _value_valid(self, value):
        try:
            int(value)
        except ValueError:
            return False
        return int(value) > 0

    def jsonrpc_sendTokens(self, address, value, requestId):
        """
        Sends value number of ZEEW to address
        """
        logging.info(f'Received a request {requestId}')
        return self.send_tokens(address, int(value), requestId)

    def send_tokens(self, address, value, req_id):
        if not self._address_valid(address):
            return 'Invalid address'
        if not self._value_valid(value):
            return 'Invalid value'

        logging.info('Sending tasks')

        (tasks.send_tokens.s(address, value, req_id)
         | tasks.get_status.s().set(countdown=60*int(mining_time))
         | tasks.save_tx_status.s()
         | tasks.send_report.s()
         )()

        return 'ok'

    def run(self):
        logger.info("Starting a server")
        signal.signal(signal.SIGUSR1, handle_pdb)
        reactor.listenTCP(7080, server.Site(SendTokensServer()))
        reactor.run()
