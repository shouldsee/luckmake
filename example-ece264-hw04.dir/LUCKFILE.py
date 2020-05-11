
from luck.shorts import RNS,DNS,ACMD,MFP,LSC, FSC
from luck.shorts import NCR,TSSR
from luck.types import TimeSizeStampRule as RULE
from luck.types import NoCacheRule
#
ns = RNS.subclass('MainRNS')()
patterns = DNS.subclass('PatternNS')()

WARNING = "-Wall -Wshadow --pedantic -Wno-unused-variable"
ERROR = "-Wvla -Werror"
TESTFALGS = "-DTEST_COUNTCHAR -DTEST_PRINTCOUNTS"

GCC = f"gcc -std=c99 -g {WARNING} {ERROR} {TESTFALGS}"

SRCS = "main.c filechar.c"
OBJS = ' '.join([x[:-2]+'.o' for x in SRCS.split()])


RULE.MWF(ns, OBJS, SRCS,  ACMD(patterns))
RULE.MWF(ns, SRCS, None,  None)

MFP.MWF(patterns,
	0, '%.o','%.c', 
	'''
	{GCC} {TESTFALGS} -c {c.i[0]} -o {c.o[0]}
	'''
	)

	# lambda c: LSC(f'{GCC} {TESTFALGS} -c {c.i[0]} -o {c.o[0]}'))


RULE.MWF(ns, 'test1',  './hw04',  
	'''
	{c.i[0]} inputs/2016 > output16
	diff output16 expected/expected16
	echo [passed] test1
	''')

RULE.MWF(ns, 'test2',  './hw04', 
	'''
	{c.i[0]} inputs/2017 > output17
	diff output17 expected/expected17
	''')

RULE.MWF(ns, 'test3', './hw04', 
	'''
	{c.i[0]} inputs/2018 > output18
	diff output18 expected/expected18
	''')

RULE.MWF(ns, 'test4', './hw04', 
	'''
	{c.i[0]} inputs/2019 > output19
	diff output19 expected/expected19
	''')

RULE.MWF(ns, 'testall', 'test1 test2 test3 test4')

RULE.MWF(ns, './hw04', OBJS, 
	'''
	{GCC} {TESTFALGS} {OBJS} -o {c.o[0]}
	''')

NCR.MWF(
	ns, 'clean', None, 
	# lambda c: LSC(f'''
	'''		
	rm -f hw04 *.o *.ident_yaml output??
	''')

# for k,v in ns.items():
# 	print(k,type(v))

if __name__ == '__main__':
	from luck.cli import luck_main
	luck_main(ns)


# ns['clean'].build()