proxy\_random
=============

**Proxy Random** is a tool to help small web scrapers. helping them prevent getting their ip banned from the target site.

default proxy lists are free-proxy-list.net and sslproxies.org but you can also add your desired proxy list websites and add a extractor for that website.

Installation
------------
.. code-block:: bash

    $ pip install proxy-random


Usage
-----
here are some examples on how to use proxy-random.

**Example 1:**
.. code-block:: python

    import requests

    from proxy_random import RandomProxy

    # if you want to use a proxy to load the proxy lists
    # use this instead(rp = RandomProxy(proxy='http://example.com:8080'))
    rp = RandomProxy()
    proxies = rp.extract_proxies() # you can also use rp.proxy_query.

    # filter the US proxies which use port 80 or 443 and check if they work
    # you can filter by multiple parameters at once or provide your own filter function(s)
    workings = proxies.filter(port=[80, 443]) \
                .check_health(timeout=5).filter(working=True)

    print(workings.random().url) # print a random working proxy

    # or iterate through proxies and use them
    for proxy in workings:
        # do something with the proxy
        requests.get("https://httpbin.org/ip", proxies={"http": proxy.url, "https": proxy.url})

ProxyQuery(s) are reusable so you can filter them as many times as needed.

here is another example of how to add custom providers
**Example 2:**
.. code-block:: python

    import requests
    from bs4 import BeautifulSoup

    from proxy_random import RandomProxy
    from proxy_random.provider import Provider
    from proxy_random.query import ProxyQuery
    from proxy_random.proxy import Proxy

    # you can also use RandomProxy(use_defaults=False) to disable default providers
    rp = RandomProxy()
    # add a custom provider

    url = "https://free-proxy-list.net" # the url of the proxy list

    # the function used to extract proxies from the url response
    def extract_proxies(response: str) -> ProxyQuery:
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

    # then create a new instance of the Provider class
    provider = Provider(url=url, extractor=extract_proxies)
    # then add the provider to the RandomProxy instance
    rp.add_provider(provider)

    # then extract the proxies like example 1
    rp.extract_proxies()
    ...

**My own usage of this package:**
.. code-block:: python

    import requests

    from proxy_random import RandomProxy

    rp = RandomProxy(proxy="my proxy")
    proxies = rp.extract_proxies() # you can also use rp.proxy_query.

    # filter the US proxies which use port 80 or 443 and check if they work
    # you can filter by multiple parameters at once or provide your own filter function(s)
    workings = proxies.filter(custom_filters=[lambda x: x.country_code != "ir",]) \
                .limit(50).check_health(timeout=5).filter(working=True)


    proxy = workings.random()

    # use the proxy in some way
    ...

Refer to the documentation for more information about these classes.
