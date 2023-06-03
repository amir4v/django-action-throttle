from setuptools import setup

setup()

"""
Delete all files in the 'dist' folder.
Update the 'version' number in the 'version' file.

python setup.py sdist
python setup.py bdist_wheel
#
python setup.py sdist bdist_wheel

twine check dist/*

twine upload --repository pypi dist/*
#
twine upload dist/*
"""
