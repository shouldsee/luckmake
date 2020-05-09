PREFIX = "/usr/local"
PREFIX = '/home/shouldsee/.local'
DESTDIR=""

from luck.shorts import RNS,DNS,LSC,TSSR
RULE=TSSR

ns = RNS()

RULE.M(ns, 'install','all',lambda c:LSC(f'''
	install -d {DESTDIR}{PREFIX}/bin/
	install -m 755 ./bin/luckbd {DESTDIR}{PREFIX}/bin/
	install -m 755 ./bin/luck {DESTDIR}{PREFIX}/bin/
	'''))

RULE.M(ns, 'all', './bin/luckbd ./bin/luck')

RULE.M(ns, './bin/luckbd ./bin/luck', 'build.sh', lambda c:LSC(f'''
	bash build.sh
	'''))
RULE.M(ns, 'build.sh')