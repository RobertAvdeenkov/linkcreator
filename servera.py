import asyncio
import random
import httpx
c=0
lis=['r','t','y']
async def chess(name,url):
    asyncio.wait_for(10)
    print(name)

async def main():
    bb=[]
    with httpx.AsyncClient() as client:
        for i in lis:
            bb.append(chess(client, i))
        await asyncio.gather(*bb)

            

