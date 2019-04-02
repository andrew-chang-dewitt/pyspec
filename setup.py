from setuptools import setup
from setuptools import find_packages

setup(
    name='pyspec',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Click==7.0',
        'py-pub-sub @ git+git://github.com/andrew-dewitt/py-pub-sub#egg=py-pub-sub'
    ],
    entry_points='''
        [console_scripts]
        pyspec=pyspec.cli.entry:entry_point
    ''',
)
