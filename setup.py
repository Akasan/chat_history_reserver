#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="chat_history_reserver",
    author="Daisuke AKAGAWA",
    version="0.1.0",
    description="Add your description here",
    long_description=open("README.md").read() if open("README.md").read().strip() else "Add your description here",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.12",
    install_requires=[
        "pydantic>=2.11.5",
    ],
)
