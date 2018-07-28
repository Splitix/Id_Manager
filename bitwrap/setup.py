from setuptools import setup, find_packages
from os import path
from codecs import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
        requirements=f.read().splitlines()

DESC = """
# Bitwrap-io

Read Martin Fowler's description of [Event Sourcing](http://martinfowler.com/eaaDev/EventSourcing.html).

Watch an event sourcing video from [Greg Young](https://www.youtube.com/watch?v=8JKjvY4etTY).

Learn more about our deterministic approach to Blockchains at our blog [blahchain.com](http://www.blahchain.com).

"""

setup(
    name="bitwrap-io",
    version="0.3.0",
    author="Matthew York",
    author_email="myork@stackdump.com",
    description="A blockchain-style python eventstore using PostgreSQL backend",
    license='MIT',
    keywords='PNML petri-net eventstore state-machine flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    long_description=DESC,
    url="http://getbitwrap.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Database :: Database Engines/Servers",
        "License :: OSI Approved :: MIT License"
    ],
)
