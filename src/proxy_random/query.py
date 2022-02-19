"""
contains the class used to query fetched proxies
"""
import asyncio
import random
from datetime import datetime
from typing import Callable, List, Optional, Union

from proxy_random.proxy import Proxy


class ProxyQuery:
    """ProxyQuery class used to work with fetched proxies."""

    def __init__(self, proxy_list: List[Proxy]) -> None:
        """
        :param proxy_list: list of proxies
        :type proxy_list: list[Proxy]
        """
        self._proxy_list: List[Proxy] = proxy_list
        self.created_at = datetime.now()

    async def _check_health(self, test_url=None, timeout=None) -> "ProxyQuery":
        """the internal method used to check health of proxies
        don't use this method directly, instead use ProxyQuery.check_health().

        :param test_url: test url used to check health of proxies, if not provided default url will be used, defaults to None
        :type test_url: str, optional
        :param timeout: timeout used in the test request, if not provided 5 seconds will be used, defaults to None
        :type timeout: int, optional
        :return: The proxy query with updated proxies
        :rtype: ProxyQuery
        """
        tasks = []
        for proxy in self._proxy_list:
            tasks.append(asyncio.ensure_future(proxy._check_health(test_url, timeout)))
        await asyncio.gather(*tasks)
        return self

    def check_health(self, test_url=None, timeout=None) -> "ProxyQuery":
        """Check health of proxies.

        :param test_url: test url used to check health of proxies, if not provided default url will be used, defaults to None
        :type test_url: str, optional
        :param timeout: timeout used in the test request, if not provided 5 seconds will be used, defaults to None
        :type timeout: int, optional
        :return: The proxy query with updated proxies
        :rtype: ProxyQuery
        """
        asyncio.get_event_loop().run_until_complete(
            self._check_health(test_url, timeout)
        )
        return self

    def filter(  # TODO: change how this method works.
        self,
        ip: Optional[str] = None,  # kinda useless
        port: Optional[Union[int, List[int]]] = None,
        country_code: Optional[Union[str, List[str]]] = None,
        country: Optional[Union[str, List[str]]] = None,
        anonymity: Optional[Union[str, List[str]]] = None,
        google: Optional[bool] = None,
        https: Optional[bool] = None,
        verified: Optional[bool] = None,
        working: Optional[bool] = None,
        last_checked: Optional[
            Union[str, List[str]]
        ] = None,  # kinda dumb 'cause it's not parsed yet.
        custom_filters: Union[Callable, List[Callable]] = None,
    ) -> "ProxyQuery":
        """method used to filter the proxies.

        :param ip: filter the IP address (useless), defaults to None
        :type ip: str, optional
        :param country_code: filter based on the country code can be a country code or list of them, defaults to None
        :type country_code: Union[str, list[str]], optional
        :param country: filter based on country can be a country or list of them, defaults to None
        :type country: Union[str, list[str]], optional
        :param anonymity: filter based on anonymity, can be a list or string, defaults to None
        :type anonymity: Union[str, list[str]], optional
        :param google: filter based on google, defaults to None
        :type google: bool, optional
        :param https: filter based on whether it's https or not, defaults to None
        :type https: bool, optional
        :param verified: filter based on if it's tested or not (if it's tested it doesn't mean it's working for that purpose use `working` instead), defaults to None
        :type verified: bool, optional
        :param working: filter based on it's working or not(proxies should be verified use check_health before filtering based on this field), defaults to None
        :type working: bool, optional
        :param last_checked: filter based on last checked time (don't use), defaults to None
        :type last_checked: Union[ str, list[str] ], optional
        :return: returns a new ProxyQuery with filtered proxies
        :rtype: ProxyQuery
        """
        filters: List[Callable] = []
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

    def _filter(self, filters: List[Callable]) -> "ProxyQuery":
        """the internal method used to filter the proxies based on the given filters.
        don't use this method directly.

        :param filters: the filters to be used to filter the proxies
        :type filters: list[Callable]
        :return: returns a new ProxyQuery with filtered proxies
        :rtype: ProxyQuery
        """
        proxy_list = self._proxy_list[::]
        for f in filters:
            proxy_list = filter(f, proxy_list)

        return ProxyQuery(list(proxy_list))

    def order_by(self, attribute: str) -> "ProxyQuery":
        """order the proxies by the given attribute in ascending order.
        use desc() after order_by() to order in descending order.

        :param attribute: attribute to order the proxies by
        :type attribute: str
        :raises AttributeError: raises AttributeError if the attribute doesn't exist
        :return: returns a new ProxyQuery with proxies in ordered
        :rtype: ProxyQuery
        """
        try:
            if not hasattr(self._proxy_list[0], attribute):
                raise AttributeError(f"Proxy has no attribute {attribute}")

        except IndexError:
            return ProxyQuery([])

        return ProxyQuery(sorted(self._proxy_list, key=lambda x: getattr(x, attribute)))

    def asc(self) -> "ProxyQuery":
        """use after order_by() to order in descending order.
        (doesn't do anything in reality)

        :return: returns the ProxyQuery
        :rtype: ProxyQuery
        """
        return self

    def desc(self) -> "ProxyQuery":
        """reverses the proxies order.
        use after order_by() to order in descending order.


        :return: returns a new ProxyQuery with the proxies in reversed order
        :rtype: ProxyQuery
        """
        return ProxyQuery(self._proxy_list[::-1])

    def random(self) -> Proxy:
        """returns a random proxy from the ProxyQuery.

        :return: a random proxy
        :rtype: Proxy
        """

        if self._proxy_list is None or len(self._proxy_list) == 0:
            return None

        return random.choice(self._proxy_list)

    def first(self) -> Union[Proxy, None]:
        """returns the first proxy from the ProxyQuery.

        :return: first proxy in the ProxyQuery
        :rtype: Union[Proxy, None]
        """
        try:
            return self._proxy_list[0]

        except IndexError:
            return None

    def last(self) -> Union[Proxy, None]:
        """returns the last proxy from the ProxyQuery.

        :return: last proxy in the ProxyQuery
        :rtype: Union[Proxy, None]
        """
        try:
            return self._proxy_list[-1]

        except IndexError:
            return None

    def limit(self, limit: int) -> "ProxyQuery":
        """returns a new ProxyQuery with the first `limit` proxies.
        :param limit: the number of proxies to return
        :type limit: int
        :return: the first `limit` proxies
        :rtype: ProxyQuery
        """
        return ProxyQuery(self._proxy_list[:limit])

    def union(self, other: "ProxyQuery") -> "ProxyQuery":
        """returns a new ProxyQuery with the union of the proxies in the ProxyQuery and the other ProxyQuery.

        :param other: the other ProxyQuery
        :type other: ProxyQuery
        :return: the union of the proxies in the ProxyQuery and the other ProxyQuery
        :rtype: ProxyQuery
        """
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
