.PHONY: docs dist

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  init       to install the project in development mode (using virtualenv is highly recommended)"
	@echo "  dist       to build python sdist and wheel packages"
	@echo "  publish    to upload packages to Pypi website"
	@echo "  flake8     to run flake8 code checker"

init:
	pip install -e .
	pip install ipdb

dist:
	python setup.py sdist
	python setup.py bdist_wheel

publish:
	python setup.py register
	python setup.py sdist upload
	python setup.py bdist_wheel upload

flake8:
	flake8 .
