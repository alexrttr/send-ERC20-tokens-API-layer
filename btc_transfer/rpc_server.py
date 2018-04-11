from twisted.web import server
from twisted.internet import reactor
from txjsonrpc.web import jsonrpc
import os
import re

from . import tasks


class SendTokensServer(jsonrpc.JSONRPC):
    def __init__(self):
        self.eth_address = re.compile('^(0x)?[0-9a-fA-F]{40}$')
        self.rpc_port = os.environ.get('RPC_PORT', 7080)

    def _address_valid(self, address):
        return re.match(self.eth_address, address)

    def _value_valid(self, value):
        return isinstance(value, int) and value > 0

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

        (tasks.send_tokens.s(address, value, req_id)
         | tasks.get_status.s()
         | tasks.save_tx_status.s()
         | tasks.send_report.s()
         )()

        return 'ok'

    def run(self):
        reactor.listenTCP(7080, server.Site(SendTokensServer()))
        reactor.run()
