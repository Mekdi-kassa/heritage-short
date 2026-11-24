.PHONY: all film validate radiocut clean test shot help

PYTHON = python3

help:
	@echo "The Heritage Short AI Video Pipeline"
	@echo "  make film       - Run end-to-end pipeline (validate, generate, mix, export)"
	@echo "  make validate   - Validate storyboard.json against schema"
	@echo "  make radiocut   - Generate audio-only radio cut for Phase 1 user testing"
	@echo "  make shot       - Regenerate single shot: make shot SHOT=shot_06"
	@echo "  make clean      - Clear cache manifest"

film:
	$(PYTHON) run_pipeline.py --all

all: film

validate:
	$(PYTHON) pipeline/validate.py

radiocut:
	$(PYTHON) run_pipeline.py --stage radio_cut

shot:
	@if [ -z "$(SHOT)" ]; then echo "Error: Specify SHOT, e.g. make shot SHOT=shot_06"; exit 1; fi
	$(PYTHON) run_pipeline.py --shot $(SHOT)

clean:
	$(PYTHON) run_pipeline.py --clean-cache
