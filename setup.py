"""setup.py for graphyte"""
import os
from setuptools import setup, find_packages

from graphyte import __version__

LONG_DESCRIPTION = open(
    os.path.join(
        os.path.dirname(__file__),
        'README.md'
    )
).read()

setup(
    name='graphyte',
    author='Jorge Somavilla,',
    version=__version__,
    url='https://github.com/CiscoDevNet/graphyte',
    description='<{graphyte}> webdoc automation tool',
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    packages=find_packages('.'),
    install_requires=[
        'atlassian-python-api',
        'xlrd',
        'openpyxl',
        'pandas',
        'requests',
        'pyang',
        'pytest-runner'
    ],
    tests_require=[
        'pylint',
        'pytest',
        'pytest-cov'
    ],
    test_suite="graphyte/tests",
    include_package_data=True
)
