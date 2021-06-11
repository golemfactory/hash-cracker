# Hash cracker example

Example application which makes use of [`yapapi`](https://github.com/golemfactory/yapapi) and [`yagna`](https://github.com/golemfactory/yagna) to perform distributed computations in Golem network.
The task achieved here is performing a dictionary attack on a single sha256 hash.

## Hello Decentralization workshop

If you're coming here from the [workshop video](https://youtu.be/gWRqu7IvYfk) - great, welcome! To follow along the live coding example, please switch to the branch `workshop` after cloning this repo:
```
git checkout workshop
```

Useful links:
- [`yagna` development environment setup](https://handbook.golem.network/requestor-tutorials/flash-tutorial-of-requestor-development)
- [`yapapi` reference](https://handbook.golem.network/yapapi/api-reference)
- [`goth` (Golem Test Harness)](https://github.com/golemfactory/goth)

## Branches
`master` branch - contains complete example code which will be kept compatible with the latest version of `yagna`.

`workshop` branch - example code with its main functions being only placeholders. Intended to be used as a starting point when following the video live coding tutorial mentioned in `Hello Decentralization workshop` section.

`yapapi-0.5` branch - complete example code which is compatible with the version of `yapapi` and `yagna` used as part of the aforementioned video tutorial.

## Installation
Create a Python3.7+ virtual environment:
```
python3 -m venv cracker-venv
```

Activate the newly-created virtual environment:
```
source cracker-venv/bin/activate
```

With the virtual env active in your current shell, use `pip` to install dependencies:
```
pip install -r requirements.txt
```
