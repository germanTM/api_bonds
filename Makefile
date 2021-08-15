clean:##clean project temp data
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

install:##install dependencies requirements
	pip install -r requirements.txt

run:## run the docker container
	docker run --publish 7000:5000 apibonds

build:
	docker build -t apibonds .

all:##first initialization of the project
	make clean
	make install
	make build
	make run