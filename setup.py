from setuptools import setup, find_packages

from __version__ import version

setup(
    name="cloner",
    version=version,
    packages=find_packages(),
    description="Command-Line Interface to manage gitlab or github repositories.",
    author="Antonio Russi",
    author_email="antonio.russi.consulting@gmail.com",
)
