from setuptools import setup, find_packages

setup(
    name='shrimp',
    version='1.0',
    author='Neo',
    description='A lightweight datastore handler.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'],
    python_requires='>=3.6'
)