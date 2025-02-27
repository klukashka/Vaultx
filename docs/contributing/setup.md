Environment setup
Clone repository

    Via https: git clone https://github.com/klukashka/Vaultx.git
    Via ssh: git@github.com:klukashka/Vaultx.git
    Via GitHub CLI: gh repo clone klukashka/Vaultx

Install poetry

    MacOS / *nix: curl -sSL https://install.python-poetry.org | python3 -
    Windows: (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

Once Poetry is installed you can execute the following:

poetry --version

Install dev-dependencies

!!! note Assumed that you are in the directory with the project

We implemented two versions of required dependencies:

    poetry install — default dependencies that installs with package via pip.
    poetry install --with dev — dependencies that installs with package via pip AND tools for testing, deploying documentation, deploying on PyPI.

You should use the second option.
Install Act — local CI

We use Act for local CI launching.

It helps us to test Vaultx on different environments use local machines instead of GitHub Actions.
