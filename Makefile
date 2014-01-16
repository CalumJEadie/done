VERSION = 0.1.0

all: osx github

osx:
	python setup-osx.py py2app

clean:
	rm -r *.egg
	rm -r build
	rm -r dist

deploy:
	cp -rv dist/Done.app ${HOME}/Applications

github: osx
	mkdir dist/done-osx
	cp -rv dist/Done.app dist/done-osx-$(VERSION)
	zip -r dist/done-osx-$(VERSION).zip dist/done-osx-$(VERSION)