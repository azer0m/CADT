from setuptools import find_packages, setup

setup(
    name='cadtlib',
    packages=find_packages(include=['cadtlib']),
    version='0.1.0',
    description='Library containing all necessary functions for CADT',
    author='Ahmed Malik',
    license='MIT',
    install_requires=["canvasapi"]
)