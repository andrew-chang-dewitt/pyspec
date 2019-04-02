from setuptools import setup
from setuptools import find_packages

setup(
    name='pyspec',
    version='0.1.0',
    packages=find_packages(),
    dependency_links=[''],
    install_requires=[
        'Click',
        'py-pub-sub @ git+ssh://git@github.com/andrew-dewitt/py-pub-sub'
    ],
    entry_points='''
        [console_scripts]
        pyspec=pyspec.cli.entry:entry_point
    ''',
)
