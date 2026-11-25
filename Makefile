# Quality gate of personal-workflows. Run `make check` when a change is finished.

PYTHON       ?= python3
SHELLCHECK   ?= shellcheck
ACTIONLINT   ?= actionlint
MARKDOWNLINT ?= markdownlint-cli2
RUFF         ?= ruff
GITLEAKS     ?= gitleaks

SHELL_SCRIPTS := $(wildcard scripts/*.sh)

.DEFAULT_GOAL := help
.PHONY: help check lint lint-shell lint-markdown lint-actions lint-python rules test secrets skills install

help:  ## list the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-16s %s\n", $$1, $$2}'

check: lint rules test  ## everything a finished change must pass
	@echo "all checks passed"

lint: lint-shell lint-markdown lint-actions lint-python  ## all linters, read-only

lint-shell:  ## shellcheck on the scripts
	$(SHELLCHECK) -x $(SHELL_SCRIPTS)

lint-python:  ## ruff on the scripts and tests
	$(RUFF) check .
	$(RUFF) format --check .

lint-actions:  ## actionlint on the workflows
	$(ACTIONLINT) $(wildcard .github/workflows/*.yml)

lint-markdown:  ## markdownlint (.markdownlint.yaml)
	$(MARKDOWNLINT) "**/*.md" "#LICENSE.md" "#plan.md" "#.mise" "#node_modules"

rules:  ## structure checks of skills, links and rule IDs (scripts/check.py)
	$(PYTHON) scripts/check.py

test:  ## tests of the checker
	$(PYTHON) -m unittest discover -s tests -v

secrets:  ## gitleaks over the working tree (.gitleaks.toml)
	$(GITLEAKS) detect --no-git --source . --redact

skills:  ## recreate the relative skill links in .agents/skills and .claude/skills
	scripts/link-skills.sh

install:  ## link the skills of DOMAINS="finance common" into the agent skill folders
	scripts/install.sh $(DOMAINS)
