import requests
import jsonrpclib as rpc


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


if __name__ == "__main__": 
    print(getnewaddress())
