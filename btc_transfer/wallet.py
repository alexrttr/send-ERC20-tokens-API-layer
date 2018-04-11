import json
import logging
import os
import six

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

DEFAULT_ETH_HOST = '192.168.0.45'
DEFAULT_ETH_RPC_PORT = 8545
DEFAULT_CONTRACT_ADDRESS = '0x6278ae7b2954ba53925EA940165214da30AFa261'


class WalletMetaClass(type):
    @property
    def w3(cls):
        if getattr(cls, '_WEB3', None) is None:
            from web3 import Web3, HTTPProvider

            host = os.environ.get('ETH_HOST', DEFAULT_ETH_HOST)
            port = os.environ.get('ETH_RPC_PORT', DEFAULT_ETH_RPC_PORT)
            provider = HTTPProvider('http://%s:%s' % (host, port))
            cls._WEB3 = Web3(provider)
            logging.info('geth node is connected!')
        return cls._WEB3


class EthWallet(six.with_metaclass(WalletMetaClass)):
    def _get_contract(self):
        with open('contract/abi.json', 'r') as abi_definition:
            abi = json.load(abi_definition)

        contract_addr = os.environ.get('CONTRACT_ADDR', DEFAULT_CONTRACT_ADDRESS)
        return self.w3.eth.contract(address=contract_addr, abi=abi)

    def _connect_eth_node(self):
        self.w3 = EthWallet.w3
        self.w3.eth.defaultAccount = self.w3.eth.accounts[0]
        self.contract = self._get_contract()

    def send_zeew(self, address, value):
        if not hasattr(self, 'w3'):
            self._connect_eth_node()

        transaction = {
            'gas': 200000,
            # 'gasPrice': 41,
        }

        logging.info('sending {} ZEEW to {}'.format(value, address))
        tx = self.contract.transfer(address, value).transact(transaction).hex()
        logging.info('sent tx {}'.format(tx))
        return tx

    def get_tx_status(self, tx):
        receipt = self.w3.eth.getTransactionReceipt(tx)
        if receipt is None:
            return None
        if 'status' in receipt:
            logging.info('tx {} status is {}'.format(tx, receipt['status']))
            return receipt['status'] == 1
        else
            logging.warn('There is no status field in receipt!')
            tx_info = w3.eth.getTransaction(tx)
            return receipt['gasUsed'] != tx_info['gas']
