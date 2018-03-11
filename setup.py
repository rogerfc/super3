#!/usr/bin/env python

from setuptools import setup

with open("README.md", 'r') as f:
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
    entry_points={
        'console_scripts': [
            'super3 = super3.main:main'
        ],
    },
)
