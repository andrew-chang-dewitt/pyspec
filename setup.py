from setuptools import setup
from setuptools import find_packages

setup(
    name='pyspec',
    version='1.1.0',
    packages=find_packages(exclude=["tests*", "example*"]),
    include_package_data=True,
    install_requires=[
        'Click==7.0',
        'pub-sub>=0.0.2'
    ],
    entry_points='''
        [console_scripts]
        pyspec=pyspec.cli.entry:entry_point
    ''',
)
