# -*- coding: utf-8 -*-
import io
from os.path import dirname
from os.path import join

from setuptools import find_packages, setup

from tox_test_command import ToxTestCommand
from sphinx.setup_command import BuildDoc
from version_extractor import extract_version_init

"""
PyPI configuration module.

This is prepared for easing the generation of deployment files.
"""

__license__ = 'MIT'

# Source package
_source_package = 'scrapper/'

# Test requirements
_tests_require = ['tox']


# Gets the long description from the readme
def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='darksouls-wiki-scrapper',
    packages=find_packages(),
    include_package_data=True,
    package_data={
    },
    version=extract_version_init(_source_package),
    description='A web scrapper for the Dark Souls Wiki',
    author='Bernardo Martínez Garrido',
    author_email='programming@bernardomg.com',
    license='MIT',
    url='https://github.com/Bernardo-MG/darksouls-wiki-scrapper',
    keywords=[],
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    long_description=read('README.rst'),
    install_requires=[
    ],
    tests_require=_tests_require,
    extras_require={'test': _tests_require},
    cmdclass={
        'build_docs': BuildDoc,
        'test': ToxTestCommand
    },
    python_requires='>=3.6',
)
