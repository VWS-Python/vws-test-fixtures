# Make commands for linting

SHELL := /bin/bash -euxo pipefail

.PHONY: actionlint
actionlint:
	actionlint

.PHONY: mypy
mypy:
	mypy .

.PHONY: pyright
pyright:
	pyright .

.PHONY: check-manifest
check-manifest:
	check-manifest .

.PHONY: doc8
doc8:
	doc8 .

.PHONY: ruff
ruff:
	ruff check .
	ruff format --check .

.PHONY: fix-ruff
fix-ruff:
	ruff check --fix .
	ruff format .

.PHONY: deptry
deptry:
	deptry src/

.PHONY: pylint
pylint:
	pylint src/ tests/ docs/

.PHONY: pyroma
pyroma:
	pyroma --min 10 .

.PHONY: vulture
vulture:
	vulture --min-confidence 100 --exclude _vendor --exclude .eggs .

.PHONY: linkcheck
linkcheck:
	$(MAKE) -C docs/ linkcheck SPHINXOPTS=$(SPHINXOPTS)

.PHONY: pyproject-fmt
pyproject-fmt:
	pyproject-fmt --check pyproject.toml

.PHONY: fix-pyproject-fmt
fix-pyproject-fmt:
	pyproject-fmt pyproject.toml

.PHONY: spelling
spelling:
	$(MAKE) -C docs/ spelling SPHINXOPTS=$(SPHINXOPTS)
