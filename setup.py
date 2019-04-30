from setuptools import find_packages, setup
from version import __version__

setup(
    name='pysphinx_autoindex',
    version=__version__,
    author='David Smith',
    author_email='david.smith.usc@gmail.com',
    packages=find_packages(),
)
