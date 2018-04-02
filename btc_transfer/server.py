from twisted.web import server
from twisted.internet import reactor
from txjsonrpc.web import jsonrpc
import os
import re

import tasks


class SendTokensServer(jsonrpc.JSONRPC):
    def __init__(self):
        self.eth_address = re.compile('^(0x)?[0-9a-fA-F]{40}$')
        self.rpc_port = os.environ.get('RPC_PORT', 7080)

    def _address_valid(address):
        return re.match(self.eth_address, address)
    
    def _value_valid(value):
        return value > 0

    def jsonrpc_sendTokens(self, address, value, requestId):
        """
        Sends value number of eth to address
        """
        try:
            return send_eth(address, value, requestId)
        except RuntimeError as ex:
            return 'error: %s' % ex.message

    def send_eth(address, value, req_id):
        if not _address_valid(address):
            return 'Invalid address'
        if not _value_valid(value):
            return 'Invalid value'

        tasks.send_tokens.apply_async(args=[address, value, requestId])
        return 'ok'

    def run():
        reactor.listenTCP(7080, server.Site(SendTokensServer()))
        reactor.run()

