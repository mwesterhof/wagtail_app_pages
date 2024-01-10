#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "wagtail>=5.0,<5.3",
]

setup_requirements = []

test_requirements = []

setup(
    author="Marco Westerhof",
    author_email="westerhof.marco@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="Full MVC support for wagtail pages",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="wagtail_app_pages",
    name="wagtail_app_pages",
    packages=find_packages(include=["wagtail_app_pages"]),
    setup_requires=setup_requirements,
    test_suite="tests.testproject.testproject.tests",
    tests_require=test_requirements,
    url="https://github.com/mwesterhof/wagtail_app_pages",
    version="0.3.5",
    zip_safe=False,
)
