from setuptools import setup

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

setup(
    name="web",
    author="me",
    version="222222.2",
    packages=["web"],
    python_requires=">=3.9.0",
    install_requires=requirements
)