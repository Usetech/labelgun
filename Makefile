build:
	poetry build

build-setuppy:
	rm ./setup.py && dephell deps convert
