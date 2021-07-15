build-base-img:
	docker build -f ./base.Dockerfile -t registry.usetech.ru/pub/labelgun/ci:base .

build-dev-img:
	docker build --build-arg CURRENT_ENV=dev -t registry.usetech.ru/pub/labelgun/ci:develop .

build:
	poetry build

build-setuppy:
	rm ./setup.py && dephell deps convert
