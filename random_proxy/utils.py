import requests
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


def check_proxy_health(proxy, test_url: str = None, timeout: int = None) -> bool:
    """
    Check the proxy health.
    """
    if test_url is None:
        test_url = TEST_URL

    if timeout is None:
        timeout = 1

    try:
        res = requests.get(
            test_url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "*/*",
            },
            proxies={
                "http": f"http://{proxy.ip}:{proxy.port}",
                "https": f"http://{proxy.ip}:{proxy.port}",
            },
            timeout=timeout,
        )
        if res.status_code == 200:
            return True

    except:
        pass
    return False
