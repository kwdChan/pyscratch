from setuptools import setup, find_packages

setup(
    name='pyscratch',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pymunk<7',
        'pygame',
        'numpy',
        'typing_extensions'
    ]
)
