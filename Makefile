view: docs
	open doc/_build/html/index.html

docs: webpage html

html:
	$(MAKE) -C doc html

webpage:
	python ./webpage.py

clean:
	find . -name "*.pyc" | xargs rm
