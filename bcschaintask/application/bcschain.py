import json
import logging
from jsonrpclib import jsonrpc
import requests
import jsonrpclib as rpc

from pycoin.networks.bitcoinish import create_bitcoinish_network
from pycoin.coins.tx_utils import create_tx
from pycoin.coins.bitcoin.Tx import Spendable
from pycoin.encoding.hexbytes import b2h, h2b, h2b_rev
from pycoin.solve.utils import build_hash160_lookup
from pycoin.ecdsa.secp256k1 import secp256k1_generator

class BCSNetManager:
    def __init__(self) -> None:

        self.rpcurl = 'http://bcs_tester:iLoveBCS@45.32.232.25:3669'
        self.apiurl = 'https://bcschain.info/api'
        self.bcswalletaddress = 'BJcL7XCT7Ju5Yv2R6Bz8gt8CWHroomagWd'

        self.network = create_bitcoinish_network(
            symbol="BCS", network_name="BCS", subnet_name="mainnet",
            wif_prefix_hex="80", address_prefix_hex="19",
            pay_to_script_prefix_hex="32", bip32_prv_prefix_hex="0488ade4",
            bip32_pub_prefix_hex="0488B21E", bech32_hrp="bc", bip49_prv_prefix_hex="049d7878",
            bip49_pub_prefix_hex="049D7CB2", bip84_prv_prefix_hex="04b2430c",
            bip84_pub_prefix_hex="04B24746", magic_header_hex="F1CFA6D3", default_port=3666
        )   

        self.rpcproxy = jsonrpc.ServerProxy(self.rpcurl)


    def getutxo(self):
        try:
            return json.loads(requests.get(f'{self.apiurl}/address/{self.bcswalletaddress}/utxo').text)[0]
        except Exception as err:
            return {"error": err}

    def sendrawtransaction(self, raw_hex: str):
        try:
            return self.rpcproxy.sendrawtransaction(raw_hex)
        except jsonrpc.TransportError as err:
            return {"error": err}

    def getnewaddress(self):
        try:
            return self.rpcproxy.getnewaddress()
        except jsonrpc.TransportError as err:
            return {"error": err}

    def decoderawtransaction(self, raw_hex: str):
        try:
            return self.rpcproxy.decoderawtransaction(raw_hex)
        except jsonrpc.TransportError as err:
            return {"error": err}

    def createsignedtx(self, secret_key: str, payables: list = [], buildhash: callable = build_hash160_lookup, generators: list = [secp256k1_generator]):
        utxo = self.getutxo()
        
        spendables = [Spendable(
                  coin_value = int(utxo['value']),
                  script = h2b(utxo['scriptPubKey']), 
                  tx_hash = h2b_rev(utxo['transactionId']), 
                  tx_out_index=int(utxo['outputIndex'])
        )]

        payables.append((self.bcswalletaddress, int(utxo['value'] - 10**8)))
        unsigned_tx = create_tx(self.network, spendables, payables, fee="standart")
        wif = self.network.parse.wif(secret_key)
        exponents = [wif.secret_exponent()]
        solver = buildhash(exponents, generators)

        return unsigned_tx.sign(solver).as_hex()    