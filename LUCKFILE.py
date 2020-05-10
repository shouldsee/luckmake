PREFIX = "/usr/local"
PREFIX = '~/.local'
DESTDIR=""

from luck.shorts import RNS,DNS,LSC,TSSR
from luck.types import NoCacheRule

RULE=TSSR

ns = RNS()

RULE.M(ns, 'install','all',lambda c:LSC(f'''
	install -d {DESTDIR}{PREFIX}/bin/
	install -m 755 ./bin/luckbd {DESTDIR}{PREFIX}/bin/
	install -m 755 ./bin/luck {DESTDIR}{PREFIX}/bin/
	'''))

RULE.M(ns, 'all', 'build')
RULE.M(ns, 'build','./bin/luckbd ./bin/luck')

RULE.M(ns, 'luck/types.py')
RULE.M(ns, './bin/luckbd ./bin/luck', 'luck/types.py', lambda c:LSC(f'''
	python3.7 -m PyInstaller cli.spec --distpath ./bin --clean
	'''))
RULE.M(ns, 'build.sh')
RULE.M(ns, 'error',  '',lambda c:LSC('echo 1231243231 && false'))
# hi && false'))

RULE.M(ns, 'pybuild','',lambda c:LSC('pip3 install . --user && pytest . && rm bin -rf'))


RULE.M(ns,'example-ece264-hw04.dir',None)
NoCacheRule.M(ns, 'time', 'example-ece264-hw04.dir', lambda c: print(LSC('''
cd example-ece264-hw04.dir
unset time
alias time=/usr/bin/time

exec 3<>/dev/null
{
	time {
	make clean    
	make testall  
	} 1>&3 2>&3

	time {
	luckbd clean
	luckbd testall
	} 1>&3


	time {
	pyluckbd clean
	pyluckbd testall
	} 1>&3 

} 2>&1
echo [finish]
exit 0
''')))

NoCacheRule.M(ns, 'test.sh', '',lambda c:print(LSC('''
cd example-ece264-hw04.dir/
python3.7 README-example.py build ./hw04
''')))
NoCacheRule.M(ns, 'count-line', '', lambda c:print(LSC('wc example-ece264-hw04.dir/{*E.py,Makefile} -c')))
