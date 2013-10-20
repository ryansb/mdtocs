#!/bin/env python
# -*- coding: utf8 -*-

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

version = "0.1.0"

setup(
    name="mdtocs",
    version=version,
    description="MDTOCS: MarkDown Table Of Contents System",
    classifiers=[
        "Topic :: Text Processing :: Indexing",
        "Topic :: Text Processing :: Markup",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
    ],
    keywords="",
    author="Ryan S. Brown",
    author_email="sb@ryansb.com",
    url="http://mdtocs.rsb.io/",
    license="LGPLv3",
    packages=find_packages(
    ),
    scripts=[
        "distribute_setup.py",
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "",
    ],
    entry_points="""
    [console_scripts]
    mdtocs = mdtocs:main
    """
)
