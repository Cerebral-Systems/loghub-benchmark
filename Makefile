# Local validation entry points — mirrors the gates that .github/workflows/
# runs on every PR. Same recipes as the justfile, for users who don't have
# `just` installed.
#
# Usage:
#   make static       # 12 ci_checks against every task in tasks/
#   make oracle-nop   # harbor oracle (==1.0) + nop (==0.0) on every task
#   make unit         # pytest tools/case_builder/tests
#   make validate-all # everything above

.PHONY: default static oracle-nop unit validate-all rebuild-curated

PYTHON ?= .venv-tools/bin/python
TASKS  := $(shell ls tasks 2>/dev/null | grep -v '^\.')

default:
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) 2>/dev/null \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}' \
	  || echo "Targets: static, oracle-nop, unit, validate-all"

static: ## Run all 12 ci_checks/*.sh against every task in tasks/
	@fail=0; \
	for slug in $(TASKS); do \
	  for check in canary task-fields task-slug dockerfile-references dockerfile-sanity \
	               task-absolute-path test-file-references test-sh-sanity task-timeout \
	               instruction-timeout-match gpu-types allow-internet; do \
	    if ! bash ci_checks/check-$$check.sh tasks/$$slug >/dev/null 2>&1; then \
	      echo "FAIL $$slug :: check-$$check.sh"; \
	      fail=$$((fail+1)); \
	    fi; \
	  done; \
	done; \
	if [ $$fail -gt 0 ]; then echo ""; echo "$$fail failure(s)"; exit 1; fi; \
	count=$$(echo "$(TASKS)" | wc -w); \
	echo "static checks: $$count tasks × 12 checks all green"

oracle-nop: ## Run harbor oracle/nop on every task (slow; needs Docker)
	@: > /tmp/make-validate.log
	@: > /tmp/make-validate.err
	@echo "$(TASKS)" | tr ' ' '\n' | xargs -P 6 -I {} bash tools/validate_task.sh {} \
	  2>>/tmp/make-validate.err | tee -a /tmp/make-validate.log
	@total=$$(wc -l </tmp/make-validate.log); \
	green=$$(grep -c '^.* oracle=1.0 nop=0.0$$' /tmp/make-validate.log || true); \
	echo ""; \
	echo "oracle/nop: $$green/$$total green"; \
	if [ "$$green" != "$$total" ]; then \
	  echo "fail rows:"; \
	  grep -v 'oracle=1.0 nop=0.0$$' /tmp/make-validate.log; \
	  exit 1; \
	fi

unit: ## Run repo-invariant + gameability + case_builder/exporter unit tests
	$(PYTHON) -m pytest tests tools/case_builder/tests -q

validate-all: unit static oracle-nop ## Run every validation gate
	@echo ""
	@echo "All validation gates green."

rebuild-curated: ## Rebuild the committed v1 curated-selection manifest (needs LOGHUB_CORPUS + corpus on disk)
	@test -n "$(LOGHUB_CORPUS)" || { echo "set LOGHUB_CORPUS to your loghub-full corpus path"; exit 1; }
	$(PYTHON) -m tools.case_builder.rebuild_curated rebuild \
	  --manifest tools/case_builder/curated_selection.json \
	  --corpus-root "$(LOGHUB_CORPUS)" \
	  --output-dir tasks
