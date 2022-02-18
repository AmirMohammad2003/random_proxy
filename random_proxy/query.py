import random
from datetime import datetime
from typing import Callable, Union

from random_proxy.proxy import Proxy


class ProxyQuery:
    def __init__(self, proxy_list: list[Proxy]) -> None:
        self._proxy_list: list[Proxy] = proxy_list
        self.created_at = datetime.now()

    def check_health(self, test_url=None, timeout=None) -> "ProxyQuery":
        for proxy in self._proxy_list:
            proxy.check_health(test_url, timeout)

        return self

    def filter(  # TODO: change how this method works.
        self,
        ip: str = None,  # kinda useless
        port: Union[int, list[int]] = None,
        country_code: Union[str, list[str]] = None,
        country: Union[str, list[str]] = None,
        anonymity: Union[str, list[str]] = None,
        google: bool = None,
        https: bool = None,
        verified: bool = None,
        working: bool = None,
        last_checked: Union[
            str, list[str]
        ] = None,  # kinda dumb 'cause it's not parsed yet.
        custom_filters: Union[Callable, list[Callable]] = None,
    ) -> "ProxyQuery":
        filters: list[Callable] = []
        if ip is not None:
            filters.append(lambda x: x.ip == ip)

        if port is not None:
            if isinstance(port, int):
                filters.append(lambda x: x.port == port)

            elif isinstance(port, list):
                filters.append(lambda x: x.port in port)

            else:
                raise TypeError(f"port must be int or list[int]")

        if country_code is not None:
            if isinstance(country_code, str):
                filters.append(lambda x: x.country_code == country_code)

            elif isinstance(country_code, list):
                filters.append(lambda x: x.country_code in country_code)

            else:
                raise TypeError(f"country_code must be str or list[str]")

        if country is not None:
            if isinstance(country, str):
                filters.append(lambda x: x.country == country)

            elif isinstance(country, list):
                filters.append(lambda x: x.country in country)

            else:
                raise TypeError(f"country must be str or list[str]")

        if anonymity is not None:
            if isinstance(anonymity, str):
                filters.append(lambda x: x.anonymity == anonymity)

            elif isinstance(anonymity, list):
                filters.append(lambda x: x.anonymity in anonymity)

            else:
                raise TypeError(f"anonymity must be str or list[str]")

        if google is not None:
            filters.append(lambda x: x.google == google)

        if https is not None:
            filters.append(lambda x: x.https == https)

        if verified is not None:
            filters.append(lambda x: x.verified == verified)

        if working is not None:
            filters.append(lambda x: x.working == working)

        if last_checked is not None:
            if isinstance(last_checked, str):
                filters.append(lambda x: x.last_checked == last_checked)

            elif isinstance(last_checked, list):
                filters.append(lambda x: x.last_checked in last_checked)

            else:
                raise TypeError(f"last_checked must be str or list[str]")

        if custom_filters is not None:
            if isinstance(custom_filters, Callable):
                filters.append(custom_filters)

            elif isinstance(custom_filters, list):
                filters.extend(custom_filters)

        return self._filter(filters)

    def _filter(self, filters: list[Callable]) -> "ProxyQuery":
        proxy_list = self._proxy_list[::]
        for f in filters:
            proxy_list = filter(f, proxy_list)

        return ProxyQuery(list(proxy_list))

    def order_by(self, attribute: str) -> "ProxyQuery":
        try:
            if not hasattr(self._proxy_list[0], attribute):
                raise AttributeError(f"Proxy has no attribute {attribute}")

        except IndexError:
            return ProxyQuery([])

        return ProxyQuery(sorted(self._proxy_list, key=lambda x: getattr(x, attribute)))

    def random(self) -> Proxy:
        if self._proxy_list is None:
            return None

        return random.choice(self._proxy_list)

    def asc(self) -> "ProxyQuery":
        return self

    def desc(self) -> "ProxyQuery":
        return ProxyQuery(self._proxy_list[::-1])

    def first(self) -> Union[Proxy, None]:
        try:
            return self._proxy_list[0]

        except IndexError:
            return None

    def last(self) -> Union[Proxy, None]:
        try:
            return self._proxy_list[-1]

        except IndexError:
            return None

    def limit(self, limit: int) -> "ProxyQuery":
        return ProxyQuery(self._proxy_list[:limit])

    def union(self, other: "ProxyQuery") -> "ProxyQuery":
        return ProxyQuery(self._proxy_list + other._proxy_list)

    def __add__(self, other: "ProxyQuery") -> "ProxyQuery":
        return self.union(other)

    def __iadd__(self, other: "ProxyQuery") -> "ProxyQuery":
        self._proxy_list += other._proxy_list
        return self

    def __getitem__(self, i: Union[slice, int]) -> Proxy:
        return self._proxy_list[i]

    def __len__(self) -> int:
        return len(self._proxy_list)

    def __str__(self) -> str:
        return f"<ProxyQuery {self.created_at}>"

    def __repr__(self) -> str:
        return self.__str__()
