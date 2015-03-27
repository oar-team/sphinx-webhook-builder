# -*- coding: utf-8 -*-
import re
import os.path as op
from setuptools import setup


def read(filename):
    ''' Return the file content. '''
    with open(op.join(op.abspath(op.dirname(__file__)), filename)) as fd:
        return fd.read()


def get_version():
    return re.compile(r".*__version__ = '(.*?)'", re.S)\
             .match(read('sphinx_webhook_builder.py')).group(1)


setup(
    name='sphinx-webhook-builder',
    author='Salem Harrache',
    author_email='salem.harrache@inria.fr',
    version=get_version(),
    url='https://github.com/oar-team/sphinx-webhook-builder',
    py_modules=['sphinx_webhook_builder'],
    install_requires=[
        'flask',
    ],
    include_package_data=True,
    zip_safe=False,
    description='Build Sphinx Documentation from Github webhooks.',
    license="BSD",
    classifiers=[
        'Development Status :: 1 - Planning',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Clustering',
    ],
    entry_points='''
        [console_scripts]
        sphinx-webhook-server=sphinx_webhook_builder:main
    ''',
)
