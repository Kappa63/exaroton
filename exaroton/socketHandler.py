import websockets
import json

class socketHandler:
    def __init__(self, auth, ws):
        self.uri = ""
        self.auth = auth
        self.ws = ws
        self.connection = None

    async def connect(self):
        self.connection = await websockets.connect(self.uri, additional_headers=self.auth)
        # print("Connected to Exaroton server.")
        await self.rcvData()

    async def setStream(self, stream):
        await self.connection.send(stream)
        await self.rcvData()
        await self.rcvData()

    async def disconnect(self):
        if self.connection:
            await self.connection.close()
            # print("Connection closed.")

    async def rcvData(self):
        if not self.connection:
            raise ConnectionError("WebSocket connection is not established.")
        try:
            data = await self.connection.recv()
            return json.loads(data)
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed by server.")
            return None
        
    def setURI(self, exarotonServer):
        self.uri = f"{self.ws}/{exarotonServer}/websocket"