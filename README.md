# node-t-checker

[![Build Status](https://travis-ci.org/alastria/node-t-checker.svg?branch=master)](https://travis-ci.org/alastria/node-t-checker)
[![Coverage Status](https://coveralls.io/repos/github/javaguirre/node-t-checker/badge.svg?branch=master)](https://coveralls.io/github/javaguirre/node-t-checker?branch=master)

Application to automatically validate a node in the Alastria T network

## Install and run

```bash
docker-compose up
```

## Launch the tests

``` bash
docker-compose run --rm validator poetry run python -m pytest --cov=validator
```
