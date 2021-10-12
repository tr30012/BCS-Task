import requests
import jsonrpclib as rpc

from pycoin.networks.bitcoinish import create_bitcoinish_network
from pycoin.coins.tx_utils import create_signed_tx

RPC_URL = 'http://bcs_tester:iLoveBCS@45.32.232.25:3669'
BCS_API_URL = 'https://bcschain.info/api'
BCS_WALLET_ADDRESS = 'BJcL7XCT7Ju5Yv2R6Bz8gt8CWHroomagWd'

def getnewaddress():
    with rpc.ServerProxy(RPC_URL) as proxy:    
        answer = proxy.getnewaddress()
        return answer

def getutxo():
    response = requests.get(f'{BCS_API_URL}/address/{BCS_WALLET_ADDRESS}')
    return response.text

def create_hex64():
    from random import randint
    return ''.join([str(randint(0, 9)) for i in range(64)])

def make_transaction():
    return create_hex64()

def kwarguments(**kwargs):
    return kwargs

if __name__ == "__main__": 
    network = create_bitcoinish_network(
        symbol="BCS", network_name="BCS", subnet_name="mainnet",
        wif_prefix_hex="80", address_prefix_hex="19",
        pay_to_script_prefix_hex="32", bip32_prv_prefix_hex="0488ade4",
        bip32_pub_prefix_hex="0488B21E", bech32_hrp="bc", bip49_prv_prefix_hex="049d7878",
        bip49_pub_prefix_hex="049D7CB2", bip84_prv_prefix_hex="04b2430c",
        bip84_pub_prefix_hex="04B24746", magic_header_hex="F1CFA6D3", default_port=3666
    )




    print(network)
