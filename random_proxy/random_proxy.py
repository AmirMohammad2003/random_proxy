from typing import Union

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
        proxies: dict[str, str] = None,
    ) -> None:
        if use_defaults:
            self.proxy_providers: list[Provider] = [
                Provider(HTTP_PROXY_URL, parse_response),
                Provider(HTTPS_PROXY_URL, parse_response),
            ]

        self.verify: bool = verify
        self.test_url: Union[str, None] = test_url
        self.timeout: Union[int, None] = timeout
        self.proxies: Union[dict[str, str], None] = proxies
        self.proxy_query: ProxyQuery = ProxyQuery([])

    def add_provider(self, provider: Provider) -> None:
        if isinstance(provider, Provider):
            self.proxy_providers.append(provider)

        else:
            raise TypeError(f"provider must be a Provider")

    def extract_proxies(self) -> ProxyQuery:
        for provider in self.proxy_providers:
            provider.extract(self.proxies)
            self.proxy_query += provider.get_proxy_query()

        if self.verify:
            self.verify_proxies()

        return self.proxy_query

    def verify_proxies(self) -> None:
        for proxy in self.proxy_query:
            proxy.check_health(self.test_url, self.timeout)
