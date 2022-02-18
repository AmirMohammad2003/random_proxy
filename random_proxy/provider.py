from typing import Callable

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

    def extract(self, proxies) -> ProxyQuery:
        if self.extractor is None:
            raise ValueError(f"extractor must be set")

        res = get_page(self.url, proxies)
        self.proxies_query = self.extractor(res)

    def get_proxy_query(self) -> ProxyQuery:
        return self.proxies_query

    def __str__(self) -> str:
        return f"{self.url}"

    def __repr__(self) -> str:
        return f"<Provider {self.url}>"
