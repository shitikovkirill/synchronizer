from setuptools import find_packages, setup

setup(
    name="synchronizer",
    version="1.0",
    packages=find_packages("./sync"),
    scripts=["cli.py"],
)
