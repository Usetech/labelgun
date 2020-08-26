from os.path import abspath, dirname, join

from setuptools import setup

BASE_PATH = abspath(dirname(__file__))
REQUIRES = open(join(BASE_PATH, "requirements.txt")).read().splitlines()
TESTS_REQUIRES = open(
    join(BASE_PATH, "requirements.dev.txt")
).read().splitlines()[1:]


setup(
    name='labelgun',
    version='0.1.3',
    url='https://gitlab.usetech.ru/pub/labelgun',
    author='Aleksey Petrunnik',
    author_email='apetrunnik@usetech.ru',
    description='Library to define system events',
    packages=['labelgun'],
    install_requires=REQUIRES,
    tests_require=TESTS_REQUIRES,
)
