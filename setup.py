from os.path import abspath, dirname, join

from setuptools import setup

BASE_PATH = abspath(dirname(__file__))
REQUIRES = open(join(BASE_PATH, "requirements.txt")).read().splitlines()
TESTS_REQUIRES = open(
    join(BASE_PATH, "requirements.dev.txt")
).read().splitlines()[1:]


setup(
    name='labelgun',
    version='0.1.7',
    url='https://gitlab.usetech.ru/pub/labelgun',
    author='Aleksey Petrunnik',
    author_email='apetrunnik@usetech.ru',
    description='Library to define system events',
    packages=['labelgun', 'labelgun.integrations'],
    install_requires=REQUIRES,
    tests_require=TESTS_REQUIRES,
    extras_require={
        'logger': ['python-json-logger>=0.1.11', 'structlog~=20.1.0'],
    },
)
