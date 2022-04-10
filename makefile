lint:
	pylint pyg --rcfile=.pylintrc

type-check:
	mypy --config-file mypy.ini --show-error-codes
