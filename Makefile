TAG?=local
NAME=url-shortener

build:
	docker build . -t ${NAME}:${TAG}

run:
	docker run -p 5000:5000 ${NAME}:${TAG}

test: build
	docker run -t ${NAME}:${TAG} pytest tests.py