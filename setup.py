from setuptools import setup
from setuptools import find_packages

setup(
    name='pyspec',
    version='0.0.1',
    packages=find_packages(),
    install_requires=['Click'],
    entry_points='''
        [console_scripts]
        pyspec=pyspec.cli.entry:entry_point
    ''',
)
