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
    version="0.0.1",
    description=".pyi typing stubs generation for d42 schemas",
    install_requires=find_required(),
    entry_points={
        'console_scripts': ['d42-typing=app.main:main']
    },
    author="Anna",
    author_email="testopia13@gmail.com",
    packages=find_packages(),
    python_requires='>=3.10',
)
