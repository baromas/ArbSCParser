from web3 import Web3
from web3.middleware import geth_poa_middleware
from datetime import datetime


def main():
    provider_url = 'https://arbitrum-one.publicnode.com'
    web3 = Web3(Web3.HTTPProvider(provider_url))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    print(web3.eth.get_block(web3.eth.block_number, True))
    for i in range(23645280, web3.eth.block_number + 1):
        print(f"Current block number: {i}")
        curr_block = web3.eth.get_block(i, True)
        sc_date = datetime.fromtimestamp(curr_block['timestamp'])
        print(sc_date)
        for trans in curr_block['transactions']:
            print(f'Hash: {trans.hash.hex()}')
            print(f'From: {trans["from"]}')
            print(f'To: {trans.to}')
            if trans.to == ['0x53Bf833A5d6c4ddA888F69c22C88C9f356a41614']:
                print("Adress coincided!!!\n")
        print('\n')



if __name__ == '__main__':
    main()
