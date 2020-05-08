from LUCKFILE import (ns,)

from pprint import pprint
def test_rule_not_defined_error(ns=ns):
	'should raise UnspecifiedName recipe not found for config.h'
	from path import Path
	import luck.header
	ns = ns.copy()
	# Path('config.h').unlink_p()

	ns.pop('kstring.c',None)

	e = [None]
	try:
		(ns['kstring.o'].build())
	except Exception as _e:
		e[0] = _e
		pass
	finally:
		assert isinstance(e[0], luck.header.RuleNotDefined), repr(e[0])

	ns['kstring.c'] = None
	(ns['kstring.o'].build())
