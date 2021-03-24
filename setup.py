
# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = ''

setup(
    long_description=readme,
    name='labelgun',
    version='0.1.8',
    description='Library to define system events',
    python_requires='==3.*,>=3.6.0',
    author='Aleksey Petrunnik',
    author_email='apetrunnik@usetech.ru',
    packages=['labelgun', 'labelgun.integrations'],
    package_dir={"": "."},
    package_data={"labelgun": ["labelgun.egg-info/*.txt"]},
    install_requires=['aenum==3.*,>=3.0.0'],
    extras_require={"dev": ["dephell==0.*,>=0.8.3", "freezegun==1.0.0", "pytest==6.2.2"], "logger": ["python-json-logger==2.0.*,>=2.0.0", "structlog==20.*,>=20.0.0 || ==21.*,>=21.0.0"]},
)
