all: save_pickle view

view: docs
	open doc/_build/html/index.html

docs: webpage html

html:
	$(MAKE) -C doc html

webpage:
	python ./webpage.py

save_pickle:
	python ./data.py

copy:
	python ./copy_files.py

clean:
	find . -name "*.pyc" | xargs rm
