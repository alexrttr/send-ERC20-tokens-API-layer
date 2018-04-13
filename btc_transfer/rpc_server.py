from __future__ import absolute_import

from celery import signature
import logging
import os
import re
from twisted.web import server
from twisted.internet import reactor
from txjsonrpc.web import jsonrpc


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SendTokensServer(jsonrpc.JSONRPC):
    def __init__(self):
        self.eth_address = re.compile('^(0x)?[0-9a-fA-F]{40}$')
        self.rpc_port = os.environ.get('RPC_PORT', 7080)

    def _address_valid(self, address):
        return re.match(self.eth_address, address)

    def _value_valid(self, value):
        ## only if a fraction of token can't be sold via
        ## investment platform
        # return isinstance(value, int) and value > 0
        try:
            float(value)
        except ValueError:
            return False
        return value > 0

    def jsonrpc_sendTokens(self, address, value, requestId):
        """
        Sends value number of ZEEW to address
        """
        try:
            return self.send_tokens(address, value, requestId)
        except RuntimeError as ex:
            return 'error: %s' % ex.message

    def send_tokens(self, address, value, req_id):
        if not self._address_valid(address):
            return 'Invalid address'
        if not self._value_valid(value):
            return 'Invalid value'

        send_tokens = signature('send_tokens', args=(address, value, req_id))
        get_status = signature('task.get_status', countdown=30)
        save_tx_status = signature('task.save_tx_status')
        send_report = signature('task.send_report')

        (  send_tokens()
         | get_status()
         | save_tx_status()
         | send_report()
         )()

#       (tasks.send_tokens.s(address, value, req_id)
#        | tasks.get_status.s()
#        | tasks.save_tx_status.s().set(countdown=30)
#        | tasks.send_report.s()
#        )()

        return 'ok'

    def run(self):
        logger.info("Starting a server")
        reactor.listenTCP(7080, server.Site(SendTokensServer()))
        reactor.run()
