from typing import Callable

from aiohttp import ClientSession

from random_proxy.query import ProxyQuery
from random_proxy.utils import get_page


class Provider:
    def __init__(self, url: str, extractor: Callable = None) -> None:
        self.url: str = url
        self.extractor: Callable = extractor
        self.proxies_query: ProxyQuery = None

    def set_extractor(self, extractor: Callable) -> None:
        if isinstance(extractor, Callable):
            self.extractor = extractor

        else:
            raise TypeError(f"extractor must be callable")

    async def extract(self, session: ClientSession) -> None:
        if self.extractor is None:
            raise ValueError(f"extractor must be set")

        res = await get_page(self.url, session)
        if res is not None:
            try:
                self.proxies_query = self.extractor(res)
            except Exception as e:
                print(f"Error extracting proxies from {self.url}: {e}")

    def get_proxy_query(self) -> ProxyQuery:
        return self.proxies_query

    def __str__(self) -> str:
        return f"{self.url}"

    def __repr__(self) -> str:
        return f"<Provider {self.url}>"
