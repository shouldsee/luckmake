ifeq ($(PREFIX),)
#     PREFIX := /usr/local
	PREFIX := $(HOME)/.local
endif
DESTDIR=

install: all
	install -d $(DESTDIR)$(PREFIX)/bin/
	install -m 755 ./bin/luckbd $(DESTDIR)$(PREFIX)/bin/
	install -m 755 ./bin/luck $(DESTDIR)$(PREFIX)/bin/

all: build
build: ./bin/luckbd ./bin/luck
	:


./bin/luckbd ./bin/luck: luck/**
	python3.7 -m PyInstaller cli.spec --distpath ./bin --clean

pybuild:
	pip3 install . --user && pytest . && rm bin -rf