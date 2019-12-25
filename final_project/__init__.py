from setuptools_scm import get_version

__version__ = None
try:
    __version__ = get_version()
except:
    __version__ = "0.1.0"
