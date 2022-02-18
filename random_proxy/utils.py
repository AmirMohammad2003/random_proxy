import requests
import aiohttp
from aiohttp_proxy import ProxyConnector
from requests import Response
from requests.adapters import HTTPAdapter

from random_proxy.config import TEST_URL


def get_page(url: str, proxies: list[str] = None) -> Response:
    """
    Get the page from the url.
    """
    if proxies is None:
        proxies = {}

    with requests.Session() as session:
        adaper = HTTPAdapter(max_retries=3)
        session.mount("http://", adaper)
        session.mount("https://", adaper)
        return session.get(url, headers={"User-Agent": "Mozilla/5.0"}, proxies=proxies)


async def check_proxy_health(
    proxy,  # type: ignore[Proxy]
    test_url: str = None,
    timeout: int = None,
) -> bool:
    """
    Check the proxy health.
    """
    if test_url is None:
        test_url = TEST_URL

    if timeout is None:
        timeout = 1

    connector = ProxyConnector(
        proxy_type=proxy.type,
        host=proxy.ip,
        port=proxy.port,
    )

    try:
        async with aiohttp.ClientSession(
            connector=connector,
            headers={
                "Accept": "*/*",
            },
        ) as session:
            async with session.get(
                test_url,
                timeout=timeout,
            ) as res:
                if res.status == 200:
                    return True

    except Exception as e:
        print(e)
    return False
