#!/usr/bin/env python

from distutils.core import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
    name='super3',
    version='1.0',
    description='A module to download super3 cartoons',
    license="MIT",
    long_description=long_description,
    author='Roger Firpo',
    author_email='roger.firpo@gmail.com',
    url="",
    packages=['super3'],  # same as name
    install_requires=['requests','beautifulsoup4'],  # external packages as dependencies
    scripts=[
        'scripts/get_series']
)
