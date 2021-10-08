import requests
import jsonrpclib as rpc


RPC_URL = 'http://bcs_tester:iLoveBCS@45.32.232.25:3669'
BCS_API_URL = 'https://bcschain.info/api'
BCS_WALLET_ADDRESS = 'BJcL7XCT7Ju5Yv2R6Bz8gt8CWHroomagWd'

def getblockchaininfo():
    with rpc.ServerProxy() as proxy:    
        answer = proxy.getblockchaininfo()
        return answer

def getutxo():
    response = requests.get(f'{BCS_API_URL}/address/{BCS_WALLET_ADDRESS}')
    return response.text


if __name__ == "__main__": 
    pass
