from setuptools import setup, find_packages

setup(
    name='pyscratch',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pymunk',
        'pygame',
        'numpy'
    ]
)
