# -*- coding: utf-8 -*-

from distutils.core import setup
from txtstyle.version import VERSION

setup(
    name='TxtStyle',
    version=VERSION,
    author='Arman Sharif',
    author_email='armandino@gmail.com',
    packages=['txtstyle'],
    scripts=['txts'],
    url='https://github.com/armandino/TxtStyle',
    license='LICENSE.txt',
    description='Command line tool for prettifying  output of console programs.',
    long_description=open('README.md').read()
)

