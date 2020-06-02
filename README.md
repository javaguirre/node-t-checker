# node-t-checker

[![Build Status](https://travis-ci.org/alastria/node-t-checker.svg?branch=master)](https://travis-ci.org/alastria/node-t-checker)

Application to automatically validate a node in the Alastria T network

## Install and run

```bash
docker-compose up
```

## Launch the tests

``` bash
docker-compose run --rm validator poetry run python -m pytest --cov=validator
```
