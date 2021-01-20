# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in tms/__init__.py
from tms import __version__ as version

setup(
	name='tms',
	version=version,
	description='Management System',
	author='RSA',
	author_email='atul.teotia@tuarcoz.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
