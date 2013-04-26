SRC_DIR = umazero
TEST_DIR = tests
DOCS_DIR = docs

all: save view

view: docs
	open docs/_build/html/index.html

docs: webpage html

html:
	$(MAKE) -C docs html

webpage:
	python -c "import umazero.webpage; umazero.webpage.run()"

save:
	python -c "import umazero; umazero.saveAll()"

copy:
	python -c "import umazero; umazero.copyfiles()"

allclean: clean
	rm -rf data ;\
	rm -rf docs/contour/* ;\
	rm -rf docs/_build/* ;\

clean:
	find . -name "*.pyc" | xargs rm

test:
	python -m unittest discover -p 'test_*.py'

check:
	pep8 *.py $(SRC_DIR)/*.py $(TEST_DIR)/*.py

sync:
	$(MAKE) -C docs sync
