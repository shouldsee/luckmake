#-*- coding: future_fstrings -*- 

from luck.types import DNS,DNSUB,DelayedNameSpace
from luck.types import NoCacheRule, TimeSizeStampRule
from luck.rule_stamp import MD5StampRule
from luck.types import RuleNameSpace as RNS
from luck.types import LSC
from luck.types import MakefilePattern, AutoCmd

# ns = RNS.subclass('MainRNS')(ruleFactory=NoCacheRule)
ns = RNS.subclass('MainRNS')(ruleFactory=TimeSizeStampRule)
# ns = RNS.subclass('MainRNS')(ruleFactory=MD5StampRule)
patterns = DNSUB('PatternNS')

WARNING = "-Wall -Wshadow --pedantic -Wno-unused-variable"
ERROR = "-Wvla -Werror"
TESTFALGS = "-DTEST_COUNTCHAR -DTEST_PRINTCOUNTS"

GCC = f"gcc -std=c99 -g {WARNING} {ERROR} {TESTFALGS}"

SRCS = "main.c filechar.c"
OBJS = ' '.join([x[:-2]+'.o' for x in SRCS.split()])
ns[OBJS] = (SRCS, AutoCmd(patterns))
ns[SRCS] = (None,None, TimeSizeStampRule)

patterns[0] = MakefilePattern(
	'%.o','%.c', 
	lambda x: LSC(f'{GCC} {TESTFALGS} -c {x.inputs[0]} -o {x.outputs[0]}'))

ns['test1'] = ('./hw04', lambda c:LSC(f'''
	{c.i[0]} inputs/2016 > output16
	diff output16 expected/expected16
	echo [passed] test1
	'''))

ns['test2'] = ('./hw04', lambda c:LSC(f'''
	{c.i[0]} inputs/2017 > output17
	diff output17 expected/expected17
	'''))


ns['test3'] = ('./hw04', lambda c:LSC(f'''
	{c.i[0]} inputs/2018 > output18
	diff output18 expected/expected18
	'''))

ns['test4'] = ('./hw04', lambda c:LSC(f'''
	{c.i[0]} inputs/2019 > output19
	diff output19 expected/expected19
	'''))

ns['testall'] = ('test1 test2 test3 test4', None)

ns['./hw04'] = (f'{OBJS}',
	lambda c:LSC(f'''
		{GCC} {TESTFALGS} {OBJS} -o {c.o[0]}
		'''))

ns['clean'] = (None, 
	lambda c: LSC('''
		rm -f hw04 *.o *.ident_yaml output??
		'''), NoCacheRule)

if __name__ == '__main__':
	ns['test1'].build()
	ns['testall'].build()
	from luck.cli import luck_main
	luck_main(ns)


# ns['clean'].build()