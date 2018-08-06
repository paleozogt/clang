from setuptools import setup, dist
from os import path
import sys

if sys.version_info < (3, 0, 0):
    from io import open  # python 2 builtin open doesn't have an encoding option
# from https://packaging.python.org/guides/making-a-pypi-friendly-readme/
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# default for set_library_path
with open("clang/cindex.py", "a") as initfile:
    initfile.write(u'''
import os
import cindex
cindex.Config.set_library_path(os.path.dirname(os.path.abspath(__file__)))
''')

# get the version
version= open('version.txt').read()

setup(
    name="clang",
    author="Ethan Smith",
    author_email="ethan@ethanhs.me",
    version=version,
    url="https://github.com/ethanhs/clang",
    packages=["clang"],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
