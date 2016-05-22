#!/usr/bin/env python

from pip.req import parse_requirements
from setuptools import setup


install_reqs = parse_requirements('requirements.txt', session=False)


setup(
    name='randompy',
    version='0.1',
    description='random.org CLI',
    author='Koen Dercksen',
    author_email='mail@koendercksen.com',
    url='http://github.com/KDercksen/randompy',
    install_requires=[str(ir.req) for ir in install_reqs],
    scripts=['randompy.py'],
)
