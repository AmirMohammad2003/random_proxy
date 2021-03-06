from bs4 import BeautifulSoup

from proxy_random.proxy import Proxy
from proxy_random.query import ProxyQuery


def parse_response(response: str) -> ProxyQuery:
    """
    built-in parser for default proxy providers.
    """
    soup = BeautifulSoup(response, "html.parser")

    headings = [i.text.lower() for i in soup.find("thead").find_all("th")]

    rows = [[j.text for j in i] for i in soup.find("tbody").find_all("tr")]

    proxies = []
    for row in rows:
        proxy = Proxy()
        for i, name in enumerate(headings):
            if name == "ip address":
                proxy.ip = row[i]

            elif name == "port":
                proxy.port = int(row[i])

            elif name == "code":
                proxy.country_code = row[i]

            elif name == "last checked":
                proxy.last_checked = row[i]

            elif name in ("google", "https"):
                setattr(proxy, name, True if row[i] == "yes" else False)

            elif name in ("country", "anonymity"):
                setattr(proxy, name, row[i])

        proxies.append(proxy)

    return ProxyQuery(proxies)
