import json
import logging
import os

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

DEFAULT_GAS_LIMIT = 200000
DEFAULT_GAS_PRICE = 41000000000
DEFAULT_ETH_HOST = 'ethereum'
DEFAULT_ETH_RPC_PORT = 8545

transaction = {
    'gas': int(os.environ.get('GAS_LIMIT', DEFAULT_GAS_LIMIT)),
    'gasPrice': int(os.environ.get('GAS_PRICE', DEFAULT_GAS_PRICE)),
}


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
            self._WEB3.eth.defaultAccount = self.w3.eth.accounts[0]
            logger.info(f'Using account {self.w3.eth.defaultAccount}')
        return self._WEB3

    @property
    def token_holder_contract(self):
        if getattr(self, '_HOLDER', None) is not None:
            return self._HOLDER
        with open('contract/holder/abi.json', 'r') as abi_definition:
            abi = json.load(abi_definition)

        contract_addr = os.environ.get('HOLDER_CONTRACT_ADDR', None)
        self._HOLDER = self.w3.eth.contract(address=contract_addr, abi=abi)
        return self._HOLDER

    @property
    def crowdsale_contract(self):
        if getattr(self, '_CWS', None) is not None:
            return self._CWS
        with open('contract/crowdsale/abi.json', 'r') as abi_definition:
            abi = json.load(abi_definition)

        contract_addr = os.environ.get('CROWDSALE_CONTRACT_ADDR', None)
        self._CWS = self.w3.eth.contract(address=contract_addr, abi=abi)
        return self._CWS

    def normalize(self, address) -> str:
        return self.w3.toChecksumAddress(address)

    def send_zeew(self, addr: str, value: int) -> str:
        address = self.normalize(addr)
        logging.info(f'sending {value} ZEEW to {address}')
        tx = self.token_holder_contract.functions.transfer(address, value).transact(transaction).hex()
        logging.info('sent tx {}'.format(tx))
        return tx

    def add_to_wl(self, addr: str) -> str:
        address = self.normalize(addr)
        logging.info(f'adding {address} to whitelist')
        tx = self.crowdsale_contract.functions.addAddressToWhitelist(address).transact(transaction).hex()
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
