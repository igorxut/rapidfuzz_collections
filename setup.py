
from setuptools import (
    find_packages,
    setup
)


with open('README.md', 'r', encoding="utf8") as fh:
    long_description = fh.read()


setup(
    author="Igor Iakovlev",
    author_email="igorxut@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description="Some collections types for working with rapidfuzz library",
    install_requires=[ 'rapidfuzz >= 3.6.1', ],
    license="MIT License",
    long_description=long_description,
    long_description_content_type='text/markdown',
    name="rapidfuzz_collections",
    packages=find_packages(include=['src']),
    python_requires=">=3.12",
    url="https://github.com/igorxut/rapidfuzz_collections",
    version="0.1.0"
)
