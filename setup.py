from setuptools import setup
from setuptools import find_packages

setup(
    name='pyspec',
    version='0.1.0',
    packages=find_packages(),
    dependency_links=['https://github.com/andrew-dewitt/py-pub-sub/tarball/master#egg=py-pub-sub-0.1.0'],
    install_requires=['Click', 'py-pub-sub>=0.0.1'],
    entry_points='''
        [console_scripts]
        pyspec=pyspec.cli.entry:entry_point
    ''',
)
