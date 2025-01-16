from exaroton.exarotonWebSocket import ExarotonWebSocket
import asyncio
import os
import dotenv

env = dotenv.find_dotenv()
dotenv.load_dotenv(env)

async def main():
    a = ExarotonWebSocket(os.environ["TOKEN"], os.environ["SERVER"])
    await a.start_conn()
    print(await a.get_stats())
    print(await a.get_heap())
    print(await a.get_console_tail(4))
    print(await a.get_tick())
    await a.close_conn()
    
asyncio.run(main())