MANAGER = python

# Run the Application
.PHONY: run
run:
	uv run $(MANAGER) main.py

# Explore vvecon icons
.PHONY: icons
icons:
	uv run $(MANAGER) -m vvecon qt icons
