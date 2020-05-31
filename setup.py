# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages
from txtstyle.version import VERSION

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="TxtStyle",
    version=VERSION,
    author="Arman Sharif",
    author_email="armandino@gmail.com",
    description="Command-line tool for colorizing output of log files and console programs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/armandino/TxtStyle",
    packages = ["txtstyle"],
    license="LICENSE.txt",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
    python_requires=">=3.2, <4",
    entry_points={
        "console_scripts": ["txts = txtstyle.txts:main"],
    },
    keywords="color log console text processing",
    test_suite="tests",
    project_urls={
        "Bug Reports": "https://github.com/armandino/TxtStyle/issues",
        "Source": "https://github.com/armandino/TxtStyle",
    },
)
