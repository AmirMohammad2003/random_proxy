from aiohttp_proxy import ProxyType

from random_proxy.utils import check_proxy_health


class BaseProxy:
    def __init__(self, *args, **kwargs) -> None:
        self.ip: str = None
        self.port: int = None
        self.country_code: str = None
        self.country: str = None
        self.anonymity: str = None
        self.google: bool = False
        self.https: bool = False
        # TODO: parse last_checked for better querying.
        self.last_checked: str = None

        # whether it's verified that the proxy is working or not.
        self.verified: bool = False
        self.working: bool = False

        for argname, arg in kwargs.items():
            setattr(self, argname, arg)

        self.type: str = ProxyType.HTTPS if self.https else ProxyType.HTTP

    @property
    def url(self) -> str:
        return f"{self.ip}:{self.port}"

    async def _check_health(self, test_url=None, timeout=None) -> bool:
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
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
