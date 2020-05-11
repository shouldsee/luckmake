from .types import *
from .types import RuleNameSpace as RNS
from .types import DelayedNameSpace as DNS
from .types import TimeSizeStampRule as TSSR
from .types import LoggedShellCommand as LSC
from .types import AutoCmd as ACMD
from .types import MakefilePattern as MFP
from .types import FstringShellCommand as FSC
from .types import NoCacheRule as NCR

def DoubeCurly(s):
	return s.replace('{','{{').replace('}','}}')
DC = DoubeCurly
