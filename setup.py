#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys

if not (2, 7, ) <= sys.version_info < (3, ):
    print("bas requires Python 2.7 or later")
    raise SystemExit(1)

from setuptools import find_packages
from distutils.core import setup

from apps.settings import __version__

setup(
    name='bas',
    version=__version__,
    description='Bas : Bottle api skeleton',
    long_description="\n\n".join(
        (
            open("README.md").read(),
            open("CHANGES.md").read(),
            open("LICENSE.md").read()
        )
    ),
    author='Maillet Hugues',
    author_email='maillet.hugues.dev@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    url='https://github.com/logorn/bottle-api-skeleton/',
    platforms=['Any'],
    entry_points={
        'console_scripts': [
            'bas-server = apps.command.server:main'
        ],
    },
    packages=find_packages(
        exclude=['tests', 'tests.*', 'example', 'example.*', 'docs', 'docs.*']
    ),
    install_requires=[
        'setuptools==5.4.2',
        'bottle>=0.11.6',
        'bottle-mongo',
        'bottle-extras',
        'argparse',
        'pymongo',
        'beaker',
        'gevent',
        'itsdangerous',
        'Crypto',
        'requests',
        'simplejson',
        'pycrypto',
        'mongokit',
        'inject >1.0, <1.1',
        'argparse'
    ],
    tests_require=['pytest', 'mock'],
    extras_require={
        'ci': [
            'flake8',
            'coverage',
            'mock',
            'pytest',
            'nose',
            'behave'
        ],
        'contribute': [
            'flake8',
            'coverage',
            'mock',
            'pytest',
            'sphinx',
            'nose',
            'behave',
            'pytest-pep8',
            'nose-exclude',
            'sphinx_bootstrap_theme',
            'fabric'
        ],
    }
)
