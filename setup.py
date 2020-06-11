#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='methnet',
    version='1.0',
    author='Kendra Oudyk',
    author_email='kendra.oudyk@gmail.com',
    description='Visualizing methods in citation networks',
    long_description=long_description,
    long_description_content_type="text/markdown",
    #py_modules=['methnet'],
    packages=setuptools.find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
     )
