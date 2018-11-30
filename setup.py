from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='github',
    version='0.0.3',
    author='Michal Polovka',
    author_email='michal.polovka@gmail.com',
    description='Command line interface for GitHub',
    download_url='https://github.com/miskopo/github_cli_app',
    url='https://github.com/miskopo/github_cli_app',
    long_description='long_description',
    packages=['github'],
    entry_points={
        'console_scripts': [
            'github = github.__main__:main'
         ]
    })
