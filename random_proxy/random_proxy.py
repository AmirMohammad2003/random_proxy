import asyncio
import random
import time
from typing import Union

from aiohttp import ClientSession, TCPConnector
from aiohttp_proxy import ProxyConnector

from random_proxy.config import HTTP_PROXY_URL, HTTPS_PROXY_URL
from random_proxy.extract import parse_response
from random_proxy.provider import Provider
from random_proxy.query import ProxyQuery


class RandomProxy(object):
    def __init__(
        self,
        verify: bool = False,
        test_url: str = None,
        timeout: int = None,
        use_defaults: bool = True,
        proxy: str = None,
    ) -> None:
        random.seed(time.time())
        if use_defaults:
            self.proxy_providers: list[Provider] = [
                Provider(HTTP_PROXY_URL, parse_response),
                Provider(HTTPS_PROXY_URL, parse_response),
            ]

        self.verify: bool = verify
        self.test_url: Union[str, None] = test_url
        self.timeout: Union[int, None] = timeout

        # Optional: used for fetching proxies from a specific proxy provider
        self.proxy: Union[str, None] = proxy

        self.proxy_query: ProxyQuery = ProxyQuery([])

    def add_provider(self, provider: Provider) -> None:
        if isinstance(provider, Provider):
            self.proxy_providers.append(provider)

        else:
            raise TypeError(f"provider must be a Provider")

    def extract_proxies(self) -> ProxyQuery:
        asyncio.get_event_loop().run_until_complete(self._extract_proxies())
        return self.proxy_query

    async def _extract_proxies(self) -> ProxyQuery:
        if self.proxy is not None:
            connector = ProxyConnector.from_url(self.proxy)
        else:
            connector = TCPConnector()

        tasks = []
        async with ClientSession(connector=connector) as session:
            for provider in self.proxy_providers:
                tasks.append(asyncio.ensure_future(provider.extract(session)))

            await asyncio.gather(*tasks)

        for provider in self.proxy_providers:
            self.proxy_query += provider.get_proxy_query()

        if self.verify:
            self.proxy_query.check_health(self.test_url, self.timeout)

        return self.proxy_query
