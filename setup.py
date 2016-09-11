from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wesh',
    version='0.0.1',
    description='',
    long_description=long_description,

    url='https://github.com/tsileo/wesh',
    author='Thomas Sileo',
    author_email='t@a4.io',
    license='MIT',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points = {
        'console_scripts': ['wesh=wesh.cli:main'],
    },
    install_requires=['zeroconf'],
)
