#!/usr/bin/env python3
from setuptools import setup

setup(
    name='github_cli_app',
    version='0.1.3',
    author='Michal Polovka',
    author_email='michal.polovka@gmail.com',
    description='Command line interface for GitHub',
    download_url='https://github.com/miskopo/github_cli_app',
    url='https://github.com/miskopo/github_cli_app',
    long_description="CLI client for GitHub using APIv4 and APIv3. For details see Wiki on https://github.com/miskopo/github_cli_app/wiki",
    platforms=['linux'],
    packages=['github', 'github.common', 'github.queries'],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'github = github.__main__:main'
         ]
    })
