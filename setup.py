#!/usr/bin/env python3
from setuptools import setup

with open('requirements.txt') as req_file:
    requirements: list = req_file.readlines()

setup(
    name='github_cli_app',
    version='1.0.3',
    author='Michal Polovka',
    author_email='michal.polovka@gmail.com',
    description='Command line interface for GitHub',
    download_url='https://github.com/miskopo/github_cli_app',
    url='https://github.com/miskopo/github_cli_app',
    long_description="CLI client for GitHub using APIv4 and APIv3. For details see Wiki on "
                     "https://github.com/miskopo/github_cli_app/wiki",
    platforms=['linux'],
    license="GPL",
    install_requires=requirements,
    packages=['github', 'github.common', 'github.queries'],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'github = github.__main__:main'
        ]
    })
