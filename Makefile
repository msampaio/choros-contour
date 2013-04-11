SRC_DIR = umazero
TEST_DIR = tests
DOCS_DIR = docs

all: save_pickle view

view: docs
	open docs/_build/html/index.html

docs: webpage html

html:
	$(MAKE) -C docs html

webpage:
	python -c "import umazero.webpage; umazero.webpage.run()"

save_pickle:
	python -c "import umazero; umazero.data.run()"

copy:
	python $(SRC_DIR)/copy_files.py

clean:
	find . -name "*.pyc" | xargs rm

test:
	python -m unittest discover -p 'test_*.py'

check:
	pep8 *.py $(SRC_DIR)/*.py $(TEST_DIR)/*.py

sync:
	$(MAKE) -C docs sync
