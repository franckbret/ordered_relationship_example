#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for ordered_relationship_example"""

from setuptools import setup, find_packages
import os

version = "0.1.0"
here = os.path.abspath(os.path.dirname(__file__))

with open(
    os.path.join(here, 'README.rst'), 'r', encoding='utf-8'
) as readme_file:
    readme = readme_file.read()

with open(
    os.path.join(here, 'CHANGELOG.rst'), 'r', encoding='utf-8'
) as changelog_file:
    changelog = changelog_file.read()

requirements = [
    'sqlalchemy < 1.4.0',
    'anyblok',
    'psycopg2-binary',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='ordered_relationship_example',
    version=version,
    description="Example of ordered relationships",
    long_description=readme + '\n\n' + changelog,
    author="Franck Bret",
    author_email='Your address email (eq. you@example.com)',
    url='https://github.com/franckbret/ordered_relationship_example',
    packages=find_packages(),
    entry_points={
        'bloks': [
            'todolist=ordered_relationship_example.todolist:Todolist'
            ]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='ordered_relationship_example',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
