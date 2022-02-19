"""
contains the main class to manage providers and proxies.
"""

import asyncio
import random
import time
from typing import List, Union

from aiohttp import ClientSession, TCPConnector
from aiohttp_proxy import ProxyConnector

from proxy_random.config import HTTP_PROXY_URL, HTTPS_PROXY_URL
from proxy_random.extract import parse_response
from proxy_random.provider import Provider
from proxy_random.query import ProxyQuery


class RandomProxy(object):
    """main class used to manage providers and proxies"""

    def __init__(
        self,
        verify: bool = False,
        test_url: str = None,
        timeout: int = None,
        use_defaults: bool = True,
        proxy: str = None,
    ) -> None:
        """RandomProxy Constructor

        :param verify: whether to verify the proxies right after proxies are extracted from providers (it's not recommended) filter the proxies then use ProxyQuery.check_health(), defaults to False
        :type verify: bool, optional
        :param test_url: test url used for testing proxies(don't use this if you want to use ProxyQuery.check_health() instead pass the test_url to ProxyQuery.check_health it self), defaults to None
        :type test_url: str, optional
        :param timeout: timeout used for testing proxies(don't use this if you want to use ProxyQuery.check_health() instead pass the timeout to ProxyQuery.check_health it self), defaults to None
        :type timeout: int, optional
        :param use_defaults: whether to use default providers or not(if you don't want to use default providers you have to add your own custom providers), defaults to True
        :type use_defaults: bool, optional
        :param proxy: proxy used to fetch the providers' url(recommended if you live in a country that these websites are blocked by government or ISP), defaults to None
        :type proxy: str, optional
        """
        random.seed(time.time())
        if use_defaults:
            self.proxy_providers: List[Provider] = [
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
        """add a provider to the list of providers

        :param provider: a provider should be an instance of `Provider` class
        :type provider: Provider
        :raises TypeError: raises TypeError if provider is not an instance of `Provider` class
        """
        if isinstance(provider, Provider):
            self.proxy_providers.append(provider)

        else:
            raise TypeError(f"provider must be a Provider")

    def extract_proxies(self) -> ProxyQuery:
        """extracts the proxies from providers

        :return: a ProxyQuery object containing the proxies
        :rtype: ProxyQuery
        """
        asyncio.get_event_loop().run_until_complete(self._extract_proxies())
        return self.proxy_query

    async def _extract_proxies(self) -> ProxyQuery:
        """the internal method used to extracts the proxies from providers
        don't use this method directly, use the extract_proxies method instead.
        """
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
