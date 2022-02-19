from setuptools import setup, find_packages

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="proxy_random",
    version="0.0.1",
    author="AmirMohammad",
    author_email="amirmohammad@duck.com",
    description="A simple package to get random proxy from online proxylist sites.",
    packages=find_packages(where='src'),
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=[
        "aiohttp",
        "aiohttp-proxy",
        "beautifulsoup4",
    ],
)
