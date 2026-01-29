import asyncio
import socket
import hashlib


class PJLinkClient:
    def __init__(self, host: str, port: int = 4352, password: str | None = None):
        self._host = host
        self._port = port
        self._password = password

    async def _send_command(self, command: str) -> str:
        reader, writer = await asyncio.open_connection(self._host, self._port)

        greeting = await reader.readline()
        greeting = greeting.decode().strip()

        auth = ""
        if greeting.startswith("PJLINK 1") and self._password:
            salt = greeting.split(" ")[1]
            auth = hashlib.md5((salt + self._password).encode()).hexdigest()

        writer.write((auth + command + "\r").encode())
        await writer.drain()

        response = await reader.readline()
        writer.close()
        await writer.wait_closed()

        return response.decode().strip()

    async def get_power(self) -> bool | None:
        resp = await self._send_command("%1POWR ?")
        if "=" not in resp:
            return None
        value = resp.split("=")[1]
        return value == "1"

