.PHONY: \
	all \
	clean \
	install \
	lab \
	lint \
	py \
	rename \
	run \
	test \

### Default target(s)
all: run

### Clean up generated files
clean:
	uv clean
	rm -fr .ruff_cache .venv

### Install this tool locally
install:
	uv tool install --upgrade .

### Run Jupyter lab
lab:
	JUPYTER_CONFIG_DIR=etc uv run jupyter lab --notebook-dir=etc/notebooks

### Perform static analysis
lint:
	uv tool run ruff check --select I --fix .
	uv tool run ruff format .
	uv tool run ruff check . --fix

### Open a Python shell
py:
	PYTHONSTARTUP= uv run ipython --profile-dir=./etc/ipython

### Rename the project
rename:
	uv run etc/set_project_name.py

### Run the project
run: lint
	uv run drawit 1 2 3 null null 4 5 6

### Run unit tests
test: lint
	PYTHONBREAKPOINT="pudb.set_trace" uv run pytest -vv

