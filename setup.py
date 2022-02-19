from setuptools import setup, find_packages

from random_proxy import __version__


setup(
    name="random_proxy",
    version=__version__,
    author="AmirMohammad Ghadimi",
    description="A simple package to get random proxy from online proxylist sites.",
    packages=find_packages(),
)
