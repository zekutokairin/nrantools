#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="nrantools",
    version="0.1.0",
    author="NRAN Tools Developer",
    author_email="developer@example.com",
    description="A Python toolkit for managing New Retro Arcade:Neon content",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nrantools",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "nrantools-carts=nrantools.cartridge:main",
            "nrantools-media=nrantools.media:main",
            "nrantools-image=nrantools.image:main",
            "nrantools-verify=nrantools.verification:main",
            "nrantools-ui=nrantools.ui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "nrantools": ["resources/*", "templates/*"],
    },
)
