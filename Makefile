MANAGER = python

# Sync dependencies
.PHONY: sync
sync:
	uv sync

# Check code style
.PHONY: lint
lint:
	ruff check

# Fix code style
.PHONY: fix
fix:
	ruff check --fix

# Run the Application
.PHONY: run
run:
	uv run $(MANAGER) main.py

# Explore vvecon icons
.PHONY: icons
icons:
	uv run $(MANAGER) -m vvecon qt icons
