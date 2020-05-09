
from luck.types import ExternalFileTask, LinkedTask, TStampedLocalTarget, LoggedShellCommand, rstrip

def expand_defer(x):
	if isinstance(x, DeferredEval):
		return expand_defer(x())
		# .eval())
	elif isinstance(x, (list,tuple, set)):
		out = [ expand_defer(xx) for xx in x]
		return type(x)(out)
	elif isinstance(x, (dict,)):
		out = [(k, expand_defer(v)) for k,v in x.items()]
		return type(x)(out)
	else:
		## do nothing if is not iterable
 		return x
def DummyCallableSelf(x):
	# def _method(self):
	return lambda self: expand_defer(x)
	
dcs     = DummyCallableSelf
dumcall = DummyCallableSelf

import sys
modvar = vars(sys.modules[__name__])
class DeferredEval(object):
	def __init__(self,ns,expr):
		self.ns = ns
		self.expr  = expr
	def __call__(self):
		return eval(self.expr, self.ns)		

def current_namespace_deferred_eval(x, ns=modvar):
	return DeferredEval(ns, x)

curde = current_namespace_deferred_eval
def dumcurde(expr):
	return dumcall(curde(expr))



# , da



WARNING = "-Wall -Wshadow --pedantic -Wno-unused-variable"
ERROR = "-Wvla -Werror"
TESTFALGS = "-DTEST_COUNTCHAR -DTEST_PRINTCOUNTS"

GCC = f"gcc -std=c99 -g {WARNING} {ERROR} {TESTFALGS}"

SRCS = "main.c filechar.c".split()
OBJS = [rstrip(x,'.c')+'.o' for x in SRCS]


class test1(LinkedTask):	
	requires = dumcurde('hw04()')
	def run_body(self):
		LoggedShellCommand([ f'./{self.input()}', 'inputs/2016 > output2016','&&','diff','expected/expected16','output2016'])		

class hw04(LinkedTask):
	requires = dcs( list(map(ExternalFileTask,SRCS)))
	output   = dcs( TStampedLocalTarget('hw04') )
	def run_body(self): 
		LoggedShellCommand([GCC,   self.input(), '-o', self.output()]); 

class test2(LinkedTask):
	requires = dumcurde('hw04()')
	def run_body(self):
		LoggedShellCommand([f'./{self.input()}', 'inputs/2017 > output2017','&&','diff','expected/expected17','output2017'])		
		
class test3(LinkedTask):
	requires = dumcurde('hw04()')
	output = lambda self: TStampedLocalTarget('output2018.passed')
	def run_body(self):
		LoggedShellCommand([f'./{self.input()}', 'inputs/2018 > output2018','&&','diff','expected/expected18','output2018'])		

class test4(LinkedTask):
	requires = dumcurde('hw04()')
	output = lambda self: TStampedLocalTarget('output2019.passed')
	def run_body(self):
		LoggedShellCommand([f'./{self.input()}', 'inputs/2019 > output2019','&&','diff','expected/expected19','output2019'])		
		# super().run()



class testall(LinkedTask):
	def requires(self):return [ test1(),test2(),test3(), test4()]
	run_body = dcs(None)

class clean(LinkedTask):
	def run_body(self):
		LoggedShellCommand('rm -f hw04 *.o output* *.ident_yaml'.split())
