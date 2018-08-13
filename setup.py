import sys
from os import path
from setuptools import setup, dist
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
from setuptools.command.bdist_egg import bdist_egg as _bdist_egg

from download_deps import download_deps

if sys.version_info < (3, 0, 0):
    from io import open  # python 2 builtin open doesn't have an encoding option
# from https://packaging.python.org/guides/making-a-pypi-friendly-readme/
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

def get_plat_name_supplied(bdist):
    if bdist.plat_name_supplied:
        return bdist.plat_name
    else:
        return None

class bdist_egg(_bdist_egg):
    def run(self):
        download_deps(get_plat_name_supplied(self))
        _bdist_egg.run(self)

class bdist_wheel(_bdist_wheel):
    def run(self):
        download_deps(get_plat_name_supplied(self))
        _bdist_wheel.run(self)

setup(
    name="clang",
    author="Ethan Smith",
    author_email="ethan@ethanhs.me",
    version=open('version.txt').read(),
    url="https://github.com/ethanhs/clang",
    packages=["clang"],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    cmdclass={
        'bdist_wheel': bdist_wheel,
        'bdist_egg': bdist_egg,
    },
)
