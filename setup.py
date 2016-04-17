#!/usr/bin/env python

import glob
import os
from setuptools import setup
from setuptools.command.install import install
from distutils import sysconfig
from distutils import dir_util

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append('../' + os.path.join(path, filename))
    return paths

extra_files = package_files('giant/plugins')

setup(
    name = "giant",
    version = "1.0.0",
    description='Generate code from Open API Specs.',
    author='Sandy Chapman',
    author_email='schapman@lixar.com',
    url='https://github.com/lixar/giant',
    packages = ['giant', 'giant.giant_base'],
    package_data={'': extra_files},
    scripts = ['giant/giant'],
    license='MIT',
    install_requires=[
        'cookiecutter==1.4.0',
        'Jinja2==2.8',
        'PyYAML==3.11',
        'requests==2.7.0',
        'Yapsy==1.11.223'
    ]
)
