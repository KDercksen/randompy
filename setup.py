#!/usr/bin/env python

from pip.req import parse_requirements
from setuptools import find_packages, setup
import randompy


install_reqs = parse_requirements('requirements.txt', session=False)


setup(
    name='randompy',
    version=randompy.__version__,
    description='random.org CLI',
    author='Koen Dercksen',
    author_email='mail@koendercksen.com',
    url='http://github.com/KDercksen/randompy',
    install_requires=[str(ir.req) for ir in install_reqs],
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': ['randompy=randompy:main'],
    },
)
