# Hash cracker example

Example application which makes use of [`yapapi`](https://github.com/golemfactory/yapapi) and [`yagna`](https://github.com/golemfactory/yagna) to perform distributed computations in Golem network.
The task achieved here is performing a dictionary attack on a single sha256 hash.

## Installation
Create a Python3.7+ virtual environment:
```
python3 -m venv /path/to/environment
```

Activate the newly-created virtual environment:
```
source /path/to/environment/bin/activate
```

With the virtual env active in your current shell, install [`poetry`](https://python-poetry.org/):
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

Install dependencies:
```
poetry install --no-root
```

## Hello Decentralization workshop

If you're here for the workshop, great! To follow along the live coding example, please switch to the branch `workshop` after cloning this repo:
```
git checkout workshop
```

To set up your `yagna` development environment follow the steps here: https://handbook.golem.network/requestor-tutorials/flash-tutorial-of-requestor-development

API reference for `yapapi` can be found here: https://handbook.golem.network/yapapi/api-reference
