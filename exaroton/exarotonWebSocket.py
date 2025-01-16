from .socketHandler import socketHandler
from . import types

class ExarotonWebSocket:
    """Exaroton Class for the Web Sockets"""

    def __init__(self, token: str, serverId: str, sock: str = "wss://api.exaroton.com/v1/servers") -> None:
        """
        Exaroton Class to interface with the API

        Parameters:
            ``token`` (``str``):
                The Authentication Token from the [user page](https://exaroton.com/account/)

            ``host`` (``str``, optional):
                The Websocket URI. Defaults to "wss://api.exaroton.com/v1/servers".
        """
        self._sock = socketHandler({"Authorization": f"Bearer {token}"}, sock)
        self._sock.setURI(serverId)

    async def start_conn(self) -> None:
        """ Start the connection with the websocket
        """
        await self._sock.connect()

    async def close_conn(self) -> None:
        """ Start the connection with the websocket
        """
        await self._sock.disconnect()

    async def get_stats(self) -> types.Stats:
        """Get live RAM and CPU stats of a server 

        Returns:
            ``types.Stats``: Your server stats
        """
        await self._sock.setStream(r'{"stream":"stats","type":"start"}')
        await self._sock.rcvData()
        _data = (await self._sock.rcvData())["data"]
        await self._sock.setStream(r'{"stream":"stats","type":"stop"}')
        return types.Stats(**_data)
    
    async def get_heap(self) -> int:
        """Get live RAM stats of a server 

        Returns:
            ``int``: memory usage
        """
        await self._sock.setStream(r'{"stream":"heap","type":"start"}')
        _data = (await self._sock.rcvData())["data"]["usage"]
        await self._sock.setStream(r'{"stream":"heap","type":"stop"} ')
        return _data
    
    async def get_tick(self) -> float:
        """Get live tick time of a server 

        Returns:
            ``float``: Average tick time for the server
        """
        await self._sock.setStream(r'{"stream":"tick","type":"start"}')
        _data = (await self._sock.rcvData())["data"]["averageTickTime"]
        await self._sock.setStream(r'{"stream":"tick","type":"stop"}')
        return _data
    
    async def get_console_tail(self, tail:int=1) -> dict:
        """Get live console of a server 

        Args:
            ``tail`` (``int``): The number 1-500 of lines
        
        Returns:
            ``list``: Containing the lines
        """
        if not tail: return
        await self._sock.setStream(r'{"stream":"console","type":"start","data":{"tail":'+str(tail)+r'}}')
        
        _data = [(await self._sock.rcvData())['data'] for _ in range(tail)]
        await self._sock.setStream(r'{"stream":"console","type":"stop"}')
        return _data