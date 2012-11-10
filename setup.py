from distutils.core import setup

setup(
    name='TxtStyle',
    version='0.3.0',
    author='Arman Sharif',
    author_email='armandino@gmail.com',
    packages=['txtstyle'],
    scripts=['txts'],
    url='https://github.com/armandino/TxtStyle',
    license='LICENSE.txt',
    description='Command line tool for prettifying  output of console programs.',
    long_description=open('README.txt').read()
)
