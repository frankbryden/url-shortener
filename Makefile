TAG?=local
NAME=url-shortener

build:
	docker build . -t ${NAME}:${TAG}

run:
	docker run -p 5000:5000 ${NAME}:${TAG}

test:
	pytest tests.py