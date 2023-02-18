#!/usr/bin/env python3
import os
import re
import shutil
import sys
from io import open

from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 5)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)


version = '0.0.1'


setup(
    name='action_throttle',
    version=version,
    url='',
    license='MIT',
    description='Django Action Throttle',
    long_description=('README.md'),
    long_description_content_type='text/markdown',
    author='Amirhosein Ghorbani',
    author_email='amir4vx@gmail.com',
    packages=[],
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.5",
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ],
    project_urls={},
)
