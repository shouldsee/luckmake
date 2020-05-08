#-*- coding: future_fstrings -*- 

from .defer import (DelayedNameSpace, DNS, DNSUB)
from .defer import (RuleNameSpace)
from .defer import (BaseRule, NoCacheRule)
from .rule_stamp import (TimeSizeStampRule)
# , RNS)

from .pattern import (AutoCmd, MakefilePattern)

from lsc.logged_shell_command import LoggedShellCommand as _LSC
def LSC(*a,**kw):
	if isinstance(a[0],str):
		a = ([a[0]],) + a[1:]
	print('[LSC]',end='')
	# print(f'[LSC]{" ".join(a[0])!r},{a[1:]}')
	print(f" ".join(a[0]))
		# ,*a)
	return _LSC(*a,**kw)

