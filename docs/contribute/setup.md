# Environment setup
## Clone repository

- Via https: `git clone https://github.com/klukashka/Vaultx.git`
- Via ssh: `git@github.com:klukashka/Vaultx.git`
- Via GitHub CLI: `gh repo clone klukashka/Vaultx`

## Install poetry

- MacOS / *nix: `curl -sSL https://install.python-poetry.org | python3 -`
- Windows: `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -`

Once Poetry is installed you can execute the following:

```sh
poetry --version
```

## Install dev-dependencies

!!! note
    Assumed that you are in the directory with the project

We implemented two versions of required dependencies:

1. `poetry install` — default dependencies that installs with package via pip.
2. `poetry install --with dev` — dependencies that installs with package via pip AND tools for testing, deploying documentation, deploying on PyPI.

**You should use the second option.**
