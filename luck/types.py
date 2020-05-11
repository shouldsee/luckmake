

from .defer import (DelayedNameSpace, DNS, DNSUB)
from .defer import (RuleNameSpace, RNS)

from .defer import (
	DelayedNameSpace,DNSUB,
	RuleNameSpace,

	BaseRule,
	NoCacheRule,
	)
from .rule_stamp import (TimeSizeStampRule, MD5StampRule)
from .pattern    import (AutoCmd, MakefilePattern)

from lsc.logged_shell_command import LoggedShellCommand as _LSC
def LoggedShellCommand(*a,**kw):
	if isinstance(a[0],str):
		a = ([a[0]],) + a[1:]
	print('[LSC]',end='')
	# print(f'[LSC]{" ".join(a[0])!r},{a[1:]}')
	print(f" ".join(a[0]))
		# ,*a)
	return _LSC(*a,**kw)
LSC = LoggedShellCommand


import inspect

def FBASH(cmd):
	'''
	```
	CC = "gcc"
	FBASH('echo {CC}')
	```
	expands to -->
	```
	CC = "gcc"
	lambda c:LSC(f'echo {CC}')
	```	
	If you find FBASH() horrible in debugging, 
	replace it with the equivalent lambda c:LSC('echo') expression in source code.
	'''
	f_back = inspect.currentframe().f_back
	
	func = eval( "lambda c: LSC(f'''{0}''') ".format(cmd), f_back.f_locals, f_back.f_globals)
	return func

# class FBASH(object):
# 	_ = '''
# 	Very hard to implement 
# 	GCC = 'gcc'
# 	FBASH('echo {GCC}')
# 	 equivalent-to ->  lambda c:LSC(f'echo {GCC}')
# 	'''
# 	def __init__(self, cmd):
# 		# self.cmd = cmd
# 		# import fstr
# 		# from future_fstrings import fstring_decode
# 		# cmd = "f'''{0}'''".format(cmd)
# 		self.cmd = cmd

# 	def __call__(self, c):
# 		import inspect
# 		frame = inspect.currentframe().f_back
# 		cmd = "f'''{0}'''".format(self.cmd, )
# 		x = eval(cmd, frame.f_locals, frame.f_globals)
# 		return LSC(x)
# 		# return LSC(s.x.evaluate())
# 		# return LSC(self.func(c))



# from os import system as LSC
# import os
# def LoggedShellCommand(cmd):
# # def LSC(cmd):
# 	ret = os.system(cmd)
# 	if ret!=0:
# 		raise Exception(f'Command returned nonzero output {ret}:\n{cmd}')
# 	return ret
# LSC = LoggedShellCommand
