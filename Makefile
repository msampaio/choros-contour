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
	python ./umazero/data.py

copy:
	python ./umazero/copy_files.py

clean:
	find . -name "*.pyc" | xargs rm
