from typing import Union

from aiohttp import ClientSession
from aiohttp_proxy import ProxyConnector

from proxy_random.config import TEST_URL


async def get_page(url: str, session: ClientSession) -> Union[str, None]:
    async with session.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10,
    ) as response:
        if response.status == 200:
            return await response.text()

    return None


async def check_proxy_health(
    proxy,  # type: ignore[Proxy]
    test_url: str = None,
    timeout: int = None,
) -> bool:
    if test_url is None:
        test_url = TEST_URL

    if timeout is None:
        timeout = 5

    connector = ProxyConnector(
        proxy_type=proxy.type,
        host=proxy.ip,
        port=proxy.port,
    )

    try:
        async with ClientSession(
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

    except Exception:
        pass

    return False
