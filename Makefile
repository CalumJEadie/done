all: osx

osx:
	python setup-osx.py py2app

clean:
	rm -r *.egg
	rm -r build
	rm -r dist