# PREFIX = "/usr/local"
PREFIX = '~/.local'
DESTDIR= ""

from luck.shorts import RNS,DNS,LSC,TSSR
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
NCR.M(ns, 'install','build',lambda c:LSC(f''' 
	install -d {DESTDIR}{PREFIX}/bin/
	install -m 755 ./bin/luckbd {DESTDIR}{PREFIX}/bin/
	install -m 755 ./bin/luck {DESTDIR}{PREFIX}/bin/
	'''))

RULE.M(ns, './bin/luckbd ./bin/luck', 'luck/types.py', lambda c:LSC(f'''
	python3.7 -m PyInstaller cli.spec --distpath ./bin --clean
	### this command would produce ./bin/luckbd and ./bin/luck
	'''))

### specify external root nodes with RULE=TSSR. 
RULE.M(ns, 'luck/types.py', None)
RULE.M(ns, 'build.sh',None)


### use NCR for commands that should always execute
NCR.M(ns, 'error',  '',lambda c:LSC('echo 1231243231 && false'))
NCR.M(ns, 'pybuild','',lambda c:LSC('python3.7 -m pip install . --user && pytest . && rm bin -rf'))

TSSR.M(ns,'example-ece264-hw04.dir',None)
NCR.M(ns, 'time', 'example-ece264-hw04.dir', lambda c: print(LSC('''
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

NCR.M(ns, 'push', '', lambda c: print(LSC('''proxychains git push -f 2>&1''')))
NCR.M(ns, 'test.sh', '',lambda c:print(LSC('''
cd example-ece264-hw04.dir/
python3.7 README-example.py build ./hw04
''')))
NCR.M(ns, 'count-line', '', lambda c:print(LSC('wc example-ece264-hw04.dir/{*E.py,Makefile} -c')))
NCR.M(ns, 'clean', '',lambda c:LSC('''
	rm -rf bin/* build/*
	'''))
