"""Setup."""

from setuptools import setup, find_packages

setup(
    name="CBCentral",
    version="1.0",
    packages=find_packages(),
    install_requires=["requests>=2.24.0"],
    author="Bruno Morais",
    author_email="brunosmmm@gmail.com",
    description="Access centralized API and databases",
)
