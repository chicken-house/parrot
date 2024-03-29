# coding=utf8
import os
from os.path import join, dirname
from setuptools import find_packages, setup
from setuptools.command.install import install


def get_file_contents(filename):
    with open(join(dirname(__file__), filename)) as fp:
        return fp.read()


setup(
    name='parrot',
    version="2.0.0",
    description="parrot背单词工具",
    long_description=get_file_contents('README.md'),
    author="Normal Cock",
    author_email="daedae11@126.com",
    url='https://github.com/chicken-house/parrot',
    install_requires=[
        'SQLAlchemy==1.4.34',
        'alembic==1.7.7',
        'numpy==1.26.4',
    ],
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    entry_points={
        'console_scripts': ['parrot=parrot_v2.cmd:run'],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
