# Endless Prime

I just started this dumb idea based on [3Blue1Brown](https://www.youtube.com/watch?v=EK32jo7i5LQ).

What is the dumb idea?

Launch a web server which is running to calculate the next prime to plot them as polar coordinates.

## Flaws

The asynchronous process might be absolutely garbage and is absolutely not safe.
I had several instances where the calculation of the coordinates crashed the global variables.

## How it looks:

![screenshot](assets/prime_13687.png)

## How to Install & Run

Just simple Dev Environment or Use Poetry

### Simple

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### poetry

```bash
poetry install
poetry shell
```

### Run

```bash
python endless_prime/server.py
```