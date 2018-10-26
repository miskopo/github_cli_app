from setuptools import setup

setup(
    name='github',
    version='0.0.1',
    packages=['github'],
    entry_points={
        'console_scripts': [
            'github = github.__main__:main'
         ]
    })
