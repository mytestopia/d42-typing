from __future__ import annotations

from setuptools import find_packages, setup


def find_required():
    with open('requirements.txt') as f:
        return f.read().splitlines()


def find_dev_required():
    with open("requirements-dev.txt") as f:
        return f.read().splitlines()


setup(
    name="d42-typing",
    version="0.0.3",
    description=".pyi typing stubs generation for d42 schemas",
    url="https://github.com/mytestopia/d42-typing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=find_required(),
    tests_require=find_dev_required(),
    entry_points={
        'console_scripts': ['d42-typing=app.main:main']
    },
    author="Anna",
    author_email="testopia13@gmail.com",
    packages=find_packages(exclude=["tests"]),
    python_requires='>=3.10',
    license="Apache-2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
