
from setuptools import setup, find_packages

setup(
  name="pip-tree",
  version="0.1.0",
  description="Dump installed package info by pip.",
  author="tikubonn",
  author_email="https://twitter.com/tikubonn",
  url="https://github.com/tikubonn/pip-tree",
  license="MIT",
  packages=find_packages(),
  entry_points={
    "console_scripts": [
      "pip-tree = pip_tree:main",
    ],
  },
)
