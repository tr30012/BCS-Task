import json
from jsonrpclib import jsonrpc
import requests
import jsonrpclib as rpc

from pycoin.networks.bitcoinish import create_bitcoinish_network
from pycoin.coins.tx_utils import create_tx
from pycoin.coins.bitcoin.Tx import Spendable
from pycoin.encoding.hexbytes import b2h, h2b, h2b_rev
from pycoin.solve.utils import build_hash160_lookup
from pycoin.ecdsa.secp256k1 import secp256k1_generator

RPC_URL = 'http://bcs_tester:iLoveBCS@45.32.232.25:3669'
BCS_API_URL = 'https://bcschain.info/api'
BCS_WALLET_ADDRESS = 'BJcL7XCT7Ju5Yv2R6Bz8gt8CWHroomagWd'

def getnewaddress():
    with rpc.ServerProxy(RPC_URL) as proxy:    
        answer = proxy.getnewaddress()
        return answer

def getutxo():
    response = requests.get(f'{BCS_API_URL}/address/{BCS_WALLET_ADDRESS}/utxo')
    return json.loads(response.text)[0]

def sendrawtransaction(hex_tx):
    with rpc.ServerProxy(RPC_URL) as proxy:    
        answer = proxy.sendrawtransaction(hex_tx)
        return answer

def decoderawtransaction(hex_tx):
    with rpc.ServerProxy(RPC_URL) as proxy:    
        answer = proxy.decoderawtransaction(hex_tx)
        return answer

def sendrawtransactionPost(hex_tx):
    response = requests.post(f'{BCS_API_URL}/tx/send', data=f'rawtx={hex_tx}')
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

    utxo = getutxo()

    s = Spendable(coin_value = int(utxo['value']),
                  script = h2b(utxo['scriptPubKey']), 
                  tx_hash = h2b(utxo['transactionId']), 
                  tx_out_index=int(utxo['outputIndex']))

    other = getnewaddress()

    tx = create_tx(network, [s], [(other, 1), (BCS_WALLET_ADDRESS, int(utxo['value'] / 25))], fee="standart")
    tx_hex = tx.as_hex()
    wif = network.parse.wif("Kwg1kex9gQ1nVrTLUFYUGfn1AykDWNAY1JaPurouBdgFUCn2vAdS")
    exponent = wif.secret_exponent()
    solver = build_hash160_lookup([exponent], [secp256k1_generator])

    signed_tx = tx.sign(solver)
    signed_tx_hex = signed_tx.as_hex()

    try:
        print(decoderawtransaction(signed_tx_hex))
    except jsonrpc.TransportError as err:
        print(err)

