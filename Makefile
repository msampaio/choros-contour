SRC_DIR = umazero
TEST_DIR = tests

all: save_pickle view

view: docs
	open docs/_build/html/index.html

docs: webpage html

html:
	$(MAKE) -C docs html

webpage:
	python ./umazero/webpage.py

# the saved data with save_pickle doesn't work
# directory
save_pickle:
	python $(SRC_DIR)/data.py

copy:
	python $(SRC_DIR)/copy_files.py

clean:
	find . -name "*.pyc" | xargs rm

test:
	python -m unittest discover -p 'test_*.py'

check:
	pep8 *.py $(SRC_DIR)/*.py $(TEST_DIR)/*.py

