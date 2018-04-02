import os
from web3 import Web3, HTTPProvider, IPCProvider

DEFAULT_CONTRACT_ADDRESS = '0x6278ae7b2954ba53925ea940165214da30afa261'
DEFAULT_ETH_HOST = 'ethereum'
DEFAULT_ETH_RPC_PORT = 8545


class EthWallet():
    def __init__(self):
        self.web3 = _connect_geth()
        self.contract = web3._get_contract()
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0];
        
    def _connect_geth(self):
        host = os.environ.get('ETH_HOST', DEFAULT_ETH_HOST)
        port = os.environ.get('ETH_RPC_PORT', DEFAULT_ETH_RPC_PORT) 
        return Web3(HTTPProvider('http://%s:%s' % (host, port)))

    def _get_contract(self):
        with open('factory.json', 'r') as abi_definition:
            abi = json.load(abi_definition)
     
        contract_addr = os.environ.get(CONTRACT_ADDR, DEFAULT_CONTRACT_ADDRESS)
        return web3.eth.contract(abi, contract_addr)

    def send_zeew(self, address, value):
        transaction = {
            'to': address,
            'value': value*1000000000,
            'gas': 200000,
            # 'gasPrice': 41,
        }
        return self.web3.transact(transaction)

    def get_tx_status(self, tx):
        self.web3.
