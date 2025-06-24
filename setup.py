from setuptools import setup, find_packages

setup(
    name='pyscratch',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pymunk',
        'pygame',
        'numpy',
        'typing_extensions'
    ]
)
