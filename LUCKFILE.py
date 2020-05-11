# PREFIX = "/usr/local"
PREFIX = '~/.local'
DESTDIR= ""

from luck.shorts import RNS,DNS,LSC,TSSR, DC
from luck.types import NoCacheRule as NCR


RULE=TSSR
ns = RNS()


### always use NCR for aliasing
NCR.M(ns, 'all', 'build install')  
### alias
NCR.M(ns, 'build','./bin/luckbd ./bin/luck')


_ = '''
- If you run "clean" first, then "build", then "install", the install would not happen
- If you run "clean" first, then "install", luckbd will do "build" then "install"
- this is because "build" is marked runned is the first run.
- it's important to select NCR / TSSR carefully. 
- use NCR when the output cannot be cached. This is true for any command-like rule
- use TSSR or other stamped rule when the output is one or more files. 
'''
### use LSC for bash command, f-string for string-completion
NCR.MWF(ns, 'install','build',
	''' 
	install -d {DESTDIR}{PREFIX}/bin/
	install -m 755 ./bin/luckbd {DESTDIR}{PREFIX}/bin/
	install -m 755 ./bin/luck {DESTDIR}{PREFIX}/bin/
	''')

luck_src = 'luck/**'
RULE.MWF(ns, luck_src)
RULE.MWF(ns, 'foo', luck_src, 'echo foo')


RULE.MWF(ns, './bin/luckbd ./bin/luck', luck_src, 
	'''
	python3.7 -m PyInstaller cli.spec --distpath ./bin --clean
	### this command would produce ./bin/luckbd and ./bin/luck
	''')

### specify external root nodes with RULE=TSSR. 
RULE.MWF(ns, 'luck/types.py', None)
# RULE.M(ns, 'foo', 'luck/**', lambda c:print('foo'))


### use NCR for commands that should always execute
NCR.MWF(ns, 'error',  '', 'echo 1231243231 && false')
NCR.MWF(ns, 'pybuild',luck_src, 'python3.7 -m pip install . --user && pytest . && rm bin -rf')

TSSR.MWF(ns,'example-ece264-hw04.dir',None)
NCR.MWF(ns, 'time', 'example-ece264-hw04.dir', 
DC('''
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
'''))


NCR.MWF(ns, 'push', '', '''proxychains git push -f 2>&1''')
NCR.MWF(ns, 'test.sh', '', 
'''
cd example-ece264-hw04.dir/
python3.7 README-example.py build ./hw04
''')
NCR.MWF(ns, 'count-line', '', 'wc example-ece264-hw04.dir/{*E.py,Makefile} -c')
NCR.MWF(ns, 'clean', '','''
	rm -rf bin/* build/*
	''')

'cat -n test/pointer/Makefile && make -C test/pointer/ result.bar'
