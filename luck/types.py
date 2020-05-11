

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

from .shell import LoggedShellCommand, FstringShellCommand