from distutils.core import setup

setup(
    name='TxtStyle',
    version='0.1.1',
    author='Arman Sharif',
    author_email='armandino@gmail.com',
    packages=['txtstyle'],
    scripts=['bin/txts'],
    url='https://github.com/armandino/TxtStyle',
    license='LICENSE.txt',
    description='Command line tool for prettifying  output of console programs.',
    long_description=open('README.txt').read(),
    install_requires=[
        "argparse >= 1.1"
    ],
)
