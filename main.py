from web3 import AsyncWeb3
from web3.middleware import async_geth_poa_middleware
from datetime import datetime
import sqlconnect as sql
import asyncio


# вынести провайдер юрл и тд за пределы функции
async def parser(async_func_num, total_instances, current_block, end_block, web3):
    for i in range(current_block, end_block + 1):
        if i % total_instances == async_func_num:
            print(f"////////////////////////////////////////////////////////////////////////////////////\nCurrent block"
                  f" number: {i}")
            curr_block = await web3.eth.get_block(i, True)
            sc_date = datetime.fromtimestamp(curr_block['timestamp'])
            print(sc_date)
            for trans in curr_block['transactions']:
                print(f'Hash: {trans.hash.hex()}')
                print(f'From: {trans["from"]}')
                print(f'To: {trans.to}')
                if trans.to == '0x6C2C06790b3E3E3c38e12Ee22F8183b37a13EE55':
                    print("Adress coincided!!!\n")
                    await sql.set_matched_adress(i, sc_date, trans.hash.hex(), trans["from"], trans.to)
            print('////////////////////////////////////////////////////////////////////////////////////\n')


async def main():
    provider_url = 'https://arbitrum-one.publicnode.com'
    web3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(provider_url))
    web3.middleware_onion.inject(async_geth_poa_middleware, layer=0)

    current_block = 23645280
    end_block = await web3.eth.block_number

    total_instances = 2
    tasks = [parser(async_func_num, total_instances, current_block, end_block, web3) for async_func_num in
             range(total_instances)]
    await sql.setup_db()
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
