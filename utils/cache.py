import asyncio
import time

class Cache:
    def __init__(self, ttl: int):
        self.ttl = ttl  # Time to live in seconds
        self.store = {}
        self.lock = asyncio.Lock()
        self.expiry = {}

    async def set(self, key: str, value: any):
        async with self.lock:
            self.store[key] = value
            self.expiry[key] = time.time() + self.ttl

    async def get(self, key: str):
        async with self.lock:
            if key in self.store:
                if time.time() < self.expiry[key]:
                    return self.store[key]
                else:
                    del self.store[key]
                    del self.expiry[key]
            return None

    async def delete(self, key: str):
        async with self.lock:
            if key in self.store:
                del self.store[key]
                del self.expiry[key]

    async def clear(self):
        async with self.lock:
            self.store.clear()
            self.expiry.clear()