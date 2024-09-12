.PHONY: install
install:
	pip3 install --quiet --upgrade pip
	pip3 install --quiet -r requirements.txt -r requirements-dev.txt

.PHONY: lint
lint:
	python3 -m flake8 && python3 -m isort -m VERTICAL_HANGING_INDENT --check-only .

.PHONY: fix-imports
fix-imports:
	python3 -m isort -m VERTICAL_HANGING_INDENT .

.PHONY: clear-pyi
clear-pyi:
	sudo find . -regex '^.*\(\.pyi\)' -delete

.PHONY: test
test:
	pytest -sv