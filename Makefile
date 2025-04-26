.PHONY: test

test:
	PYTHONPATH=$(pwd)/src python -m unittest discover -s src -p "test_*.py"
