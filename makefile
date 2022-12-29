APP_NAME = aysa

requirements:
	pip install -r requirements.txt

build: requirements
	pyinstaller aysa.spec

install: build
	sudo cp dist/${APP_NAME} /usr/local/bin/

clean:
	rm -rf build/ dist/