ifeq ($(PREFIX),)
#     PREFIX := /usr/local
	PREFIX := $(HOME)/.local
endif
DESTDIR=

install: all
	install -d $(DESTDIR)$(PREFIX)/bin/
	install -m 755 ./bin/luckbd $(DESTDIR)$(PREFIX)/bin/
	install -m 755 ./bin/luck $(DESTDIR)$(PREFIX)/bin/

all: ./bin/luckbd ./bin/luck

./bin/luckbd ./bin/luck: luck/** build.sh
	bash build.sh --clean

pybuild:
	pip3 install . --user && pytest . && rm bin -rf