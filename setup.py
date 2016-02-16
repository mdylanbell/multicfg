#!/usr/bin/env python

from setuptools import setup
import sys

__VERSION__ = '0.1'


needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='multicfg',
    version=__VERSION__,
    install_requires=[
    ],
    author='Matthew Bell <m.dylan.bell@gmail.com>',
    description='A tool to load configuration of various types from multiple sources',
    long_description=readme,
    url='https://github.com/mdylanbell/multicfg',
    packages=['multicfg'],
    setup_requires=[] + pytest_runner,
    tests_require=[
        'pytest',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'License :: Other/Proprietary License',
        'Private :: Do Not Upload',  # Safety net, pypi should reject
    ],
)
