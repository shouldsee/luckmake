
from luck.types import *
_ = '''

namespace utility
=======================
RNS:    RuleNameSpace
DNSUB:  DelayedNameSpaceSUBclass
LSC:    LoggedShellCommand

callable to execute during build time
======================================
pyfunc: 
AutoCmd:
MFP:    MakeFilePattern: 

rule classes
=========================
BaseRule:
TimeSizeStampRule:
MD5StampRule:
NoCacheRule:
'''
## create RuleNameSpace and set default
ns = RNS.subclass('MainRNS')(ruleFactory=TimeSizeStampRule) 
## create patterns namespace 
patterns = DNSUB('PatternNS')

WARNING = "-Wall -Wshadow --pedantic -Wno-unused-variable"
ERROR = "-Wvla -Werror"
TESTFALGS = "-DTEST_COUNTCHAR -DTEST_PRINTCOUNTS"

GCC = f"gcc -std=c99 -g {WARNING} {ERROR} {TESTFALGS}"

SRCS = "main.c filechar.c"
OBJS = ' '.join([x[:-2]+'.o' for x in SRCS.split()]) ## pure python func!
ns[OBJS] = (SRCS, AutoCmd(patterns))
ns[SRCS] = (None,None, TimeSizeStampRule)

patterns[0] = MakefilePattern(
	'%.o','%.c', 
	lambda x: LSC(f'{GCC} {TESTFALGS} -c {x.inputs[0]} -o {x.outputs[0]}'))

ns['./hw04'] = (f'{OBJS}',
	lambda c:LSC(f'''
		{GCC} {TESTFALGS} {OBJS} -o {c.o[0]}
		'''))
### c.i, c.o instead of $< $@
ns['test1'] = ('./hw04', lambda c:LSC(f'''
	{c.i[0]} inputs/2016 > output16
	diff output16 expected/expected16
	echo [passed] test1
	'''))

if __name__ == '__main__':
	from path import Path
	with Path(__file__).realpath().dirname():
		from luck.cli import luck_main
		luck_main(ns)