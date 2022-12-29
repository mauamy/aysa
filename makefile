requirements:
	pip install -r requirements.txt

build: requirements
	pyinstaller --onefile main.py --name tts

install: build
	sudo cp dist/tts /usr/local/bin/

clean:
	rm -rf build/ dist/ *.spec