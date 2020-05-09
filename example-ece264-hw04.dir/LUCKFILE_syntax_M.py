#-*- coding: future_fstrings -*- 
from luck.shorts import RNS,DNS,ACMD,MFP,LSC
from luck.types import TimeSizeStampRule as RULE
from luck.types import NoCacheRule

ns = RNS.subclass('MainRNS')() 
patterns = DNS.subclass('PatternNS')()

WARNING = "-Wall -Wshadow --pedantic -Wno-unused-variable"
ERROR = "-Wvla -Werror"
TESTFALGS = "-DTEST_COUNTCHAR -DTEST_PRINTCOUNTS"

GCC = f"gcc -std=c99 -g {WARNING} {ERROR} {TESTFALGS}"

SRCS = "main.c filechar.c"
OBJS = ' '.join([x[:-2]+'.o' for x in SRCS.split()]) ## pure python func!


RULE.M(ns, OBJS, SRCS,  ACMD(patterns))
RULE.M(
	ns, SRCS, None,  None)


MFP.M(patterns,
	0, '%.o','%.c', 
	lambda c: LSC(f'{GCC} {TESTFALGS} -c {c.i[0]} -o {c.o[0]}'))


RULE.M(ns, './hw04', OBJS, lambda c:LSC(f'''
	{GCC} {TESTFALGS} {OBJS} -o {c.o[0]}
	'''))


RULE.M(ns, 'test1',  './hw04',  lambda c:LSC(f'''
	{c.i[0]} inputs/2016 > output16
	diff output16 expected/expected16
	echo [passed] test1
	'''))


if __name__ == '__main__':
	from luck.cli import luck_main
	luck_main(ns)