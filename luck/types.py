

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


# from os import system as LSC
# import os
# def LoggedShellCommand(cmd):
# # def LSC(cmd):
# 	ret = os.system(cmd)
# 	if ret!=0:
# 		raise Exception(f'Command returned nonzero output {ret}:\n{cmd}')
# 	return ret
# LSC = LoggedShellCommand
