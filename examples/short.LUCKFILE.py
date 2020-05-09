
from luck.types import ExternalFileTask, LinkedTask, TStampedLocalTarget, LoggedShellCommand, rstrip

WARNING = "-Wall -Wshadow --pedantic -Wno-unused-variable"
ERROR = "-Wvla -Werror"
TESTFALGS = "-DTEST_COUNTCHAR -DTEST_PRINTCOUNTS"

GCC = f"gcc -std=c99 -g {WARNING} {ERROR} {TESTFALGS}"
# .format(**locals())

SRCS = "main.c filechar.c".split()
OBJS = [rstrip(x,'.c')+'.o' for x in SRCS]



def DummyCallable(x):
	return lambda self: x

class hw04(LinkedTask):
	requires = dc( list(map(ExternalFileTask, SRCS)) )
	output   = dc( TStampedLocalTarget('hw04') )
	def run(self): 
		LoggedShellCommand([GCC, [x.path for x in self.input()], '-o', self.output().path]); 
		super().run()


class test1(LinkedTask):
	requires = [da(mod, 'hw04'),]
	# requires = lambda self: [hw04()]
	output   = lambda self: TStampedLocalTarget('output2016.passed')
	def run(self):
		LoggedShellCommand(['./'+self.input()[0].path, 'inputs/2016 > output2016','&&','diff','expected/expected16','output2016'])		
		super().run()