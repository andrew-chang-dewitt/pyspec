from setuptools import setup
from setuptools import find_packages

setup(
    name='pyspec',
    version='1.1.0',
    packages=find_packages(),
    install_requires=[
        'Click==7.0',
        'pub-sub @ git+git://github.com/andrew-dewitt/py-pub-sub#egg=pub-sub'
    ],
    entry_points='''
        [console_scripts]
        pyspec=pyspec.cli.entry:entry_point
    ''',
)
