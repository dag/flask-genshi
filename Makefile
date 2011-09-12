.PHONY: test cover

test:
	@python -munittest discover -s tests

cover:
	@coverage run --source flaskext.genshi -m unittest discover -s tests
	@coverage report
	@coverage html
