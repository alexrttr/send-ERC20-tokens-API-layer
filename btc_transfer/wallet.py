import json
import logging
import os

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

DEFAULT_GAS_LIMIT = 200000
DEFAULT_GAS_PRICE = 41
DEFAULT_ETH_HOST = '192.168.0.45'
DEFAULT_ETH_RPC_PORT = 8545
DEFAULT_CONTRACT_ADDRESS = '0x6278ae7b2954ba53925EA940165214da30AFa261'


class EthWallet(object):
    @property
    def w3(self):
        if getattr(self, '_WEB3', None) is None:
            from web3 import Web3, HTTPProvider

            host = os.environ.get('ETH_HOST', DEFAULT_ETH_HOST)
            port = os.environ.get('ETH_RPC_PORT', DEFAULT_ETH_RPC_PORT)
            provider = HTTPProvider('http://%s:%s' % (host, port))
            self._WEB3 = Web3(provider)
            logging.info('geth node is connected!')
        return self._WEB3

    @property
    def token_holder_contract(self):
        if getattr(self, '_HOLDER', None) is not None:
            return self._HOLDER
        with open('contract/holder/abi.json', 'r') as abi_definition:
            abi = json.load(abi_definition)

        contract_addr = os.environ.get('CONTRACT_ADDR', DEFAULT_CONTRACT_ADDRESS)
        self._HOLDER = self.w3.eth.contract(address=contract_addr, abi=abi)
        return self._HOLDER

    def send_zeew(self, address: str, value: int) -> str:
        self.w3.eth.defaultAccount = self.w3.eth.accounts[0]
        logger.info(f'Using account {self.w3.eth.defaultAccount}')

        transaction = {
            'gas': int(os.environ.get('GAS_LIMIT', DEFAULT_GAS_LIMIT)),
            'gasPrice': int(os.environ.get('GAS_PRICE', DEFAULT_GAS_PRICE)),
        }

        logging.info('sending {} ZEEW to {}'.format(value, address))
        tx = self.contract.functions.transfer(address, value).transact(transaction).hex()
        logging.info('sent tx {}'.format(tx))
        return tx

    def get_tx_status(self, tx: str) -> bool:
        receipt = self.w3.eth.getTransactionReceipt(tx)
        if receipt is None:
            return None
        if 'status' in receipt:
            logging.info(f'tx {tx} status is {receipt["status"]}')
            return receipt['status'] == 1

        logging.warn('There is no status field in receipt!')
        tx_info = w3.eth.getTransaction(tx)
        return receipt['gasUsed'] != tx_info['gas']
