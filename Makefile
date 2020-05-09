ifeq ($(PREFIX),)
    PREFIX := /usr/local
endif
DESTDIR=

install: all
	install -d $(DESTDIR)$(PREFIX)/bin/
	install -m 755 ./bin/luckbd $(DESTDIR)$(PREFIX)/bin/
	install -m 755 ./bin/luck $(DESTDIR)$(PREFIX)/bin/

all: ./bin/luckbd ./bin/luck

./bin/luckbd ./bin/luck: build.sh
	bash build.sh


