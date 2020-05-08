#-*- coding: future_fstrings -*- 

from luck.types import DNS,DNSUB,DelayedNameSpace
from luck.types import Rule, NoCacheRule
from luck.types import RuleNameSpace
from luck.types import RuleNameSpace as RNS
from luck.types import LSC
from luck.types import MakefilePattern, AutoCmd
from attrdict import AttrDict
# class TStampRule
ns = RNS.subclass('MainRNS')(ruleFactory=NoCacheRule)
patterns = DNSUB('PatternNS')

WARNING = "-Wall -Wshadow --pedantic -Wno-unused-variable"
ERROR = "-Wvla -Werror"
TESTFALGS = "-DTEST_COUNTCHAR -DTEST_PRINTCOUNTS"

GCC = f"gcc -std=c99 -g {WARNING} {ERROR} {TESTFALGS}"

SRCS = "main.c filechar.c"
OBJS = ' '.join([x[:-2]+'.o' for x in SRCS.split()])
ns[OBJS] = (SRCS, AutoCmd(patterns))

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

ns[SRCS] = None
# ns['test1'].build()
ns['testall'].build()
