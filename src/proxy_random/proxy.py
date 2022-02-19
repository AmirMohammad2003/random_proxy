"""
contains the Proxy and BaseProxy class which contains the information about proxies.
"""

from aiohttp_proxy import ProxyType

from proxy_random.utils import check_proxy_health


class BaseProxy:
    """The base proxy class"""

    def __init__(
        self,
        ip: str=None,
        port: int=None,
        country_code: str=None,
        country: str=None,
        anonymity: str=None,
        google: bool=None,
        https: bool=None,
        last_checked: str=None,
        **kwargs,
    ) -> None:
        """BaseProxy constructor, Don't use this class directly, instead use the Proxy class.

        :param ip: proxy ip address
        :type ip: str
        :param port: proxy port
        :type port: int
        :param country_code: country code
        :type country_code: str
        :param country: proxy country
        :type country: str
        :param anonymity: proxy anonymity
        :type anonymity: str
        :param google: whether it's a google proxy
        :type google: bool
        :param https: whether it's a https proxy
        :type https: bool
        :param last_checked: last checked time
        :type last_checked: str
        """

        self.ip: str = ip
        self.port: int = port
        self.country_code: str = country_code
        self.country: str = country
        self.anonymity: str = anonymity
        self.google: bool = google
        self.https: bool = https
        # TODO: parse last_checked for better querying.
        self.last_checked: str = last_checked

        # whether it's verified that the proxy is working or not.
        self.verified: bool = False
        self.working: bool = False

        for argname, arg in kwargs.items():
            setattr(self, argname, arg)

        self.type: str = ProxyType.HTTPS if self.https else ProxyType.HTTP

    @property
    def url(self) -> str:
        """the proxy url in format of ip:port

        :return: proxy url
        :rtype: str
        """
        return f"{self.ip}:{self.port}"

    async def _check_health(self, test_url=None, timeout=None) -> bool:
        """checks the proxy health by making a request to the test_url.
        should not be used directly, instead use ProxyQuery.check_health.

        :param test_url: the url to test the proxies on, if not provided the default url will be used, defaults to None
        :type test_url: str, optional
        :param timeout: timout used in the test request, if not provided 5 seconds will be used, defaults to None
        :type timeout: int, optional
        :return: returns True if the proxy is working, False otherwise
        :rtype: bool
        """
        self.verified = True
        if await check_proxy_health(self, test_url, timeout):
            self.working = True

        else:
            self.working = False

        return self.working

    def __str__(self) -> str:
        return f"{self.ip}:{self.port}"

    def __repr__(self) -> str:
        return f"<Proxy {self.ip}:{self.port}>"

    def __eq__(self, other) -> bool:
        return self.ip == other.ip and self.port == other.port


class Proxy(BaseProxy):
    """
    the main proxy object that contains all the information about the proxy
    use this class instead of BaseProxy if you want to use the proxy object.
    it's most likely that you won't use this class directly if you use the default providers.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
