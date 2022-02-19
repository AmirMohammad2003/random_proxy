"""
contains the provider class which is used to register a provider and parse the response.
"""
from typing import Callable

from aiohttp import ClientSession

from proxy_random.query import ProxyQuery
from proxy_random.utils import get_page


class Provider:
    """The proxy provider class"""

    def __init__(self, url: str, extractor: Callable = None) -> None:
        """Provider Constructor

        :param url: the website url to fetch proxies from
        :type url: str
        :param extractor: the extractor function used to parse the response, must be provided when provider is actually used to retrieve proxies, defaults to None
        :type extractor: Callable, optional
        """
        self.url: str = url
        self.extractor: Callable = extractor
        self.proxies_query: ProxyQuery = ProxyQuery([])

    def set_extractor(self, extractor: Callable) -> None:
        """used to set the extractor function if not provided in the constructor.

        :param extractor: the extractor function.
        :type extractor: Callable
        :raises TypeError: raises TypeError if extractor is not a function
        """
        if isinstance(extractor, Callable):
            self.extractor = extractor

        else:
            raise TypeError(f"extractor must be callable")

    async def extract(self, session: ClientSession) -> None:
        """the method used to extract proxies from the provider.
        shouldn't be used directly, use the extract_proxies method in RandomProxy class instead.

        :param session: session used to fetch the url
        :type session: ClientSession
        :raises ValueError: raises ValueError if the extractor function is not provided.
        """
        if self.extractor is None:
            raise ValueError(f"extractor must be set")

        res = await get_page(self.url, session)
        if res is not None:
            try:
                self.proxies_query = self.extractor(res)
            except Exception as e:
                print(f"Error extracting proxies from {self.url}: {e}")

    def get_proxy_query(self) -> ProxyQuery:
        """returns the proxy query object.

        :return: the proxy query object
        :rtype: ProxyQuery
        """
        return self.proxies_query

    def __str__(self) -> str:
        return f"{self.url}"

    def __repr__(self) -> str:
        return f"<Provider {self.url}>"
