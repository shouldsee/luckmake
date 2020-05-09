from attrdict import AttrDict as _AttrDict
__version__ = '0.0.2'
PACKAGE_NAME = 'luck'
class RuleNotDefined(Exception):
	pass

class SetAttrDenied(Exception):
	pass

class AttrDict(_AttrDict):
	_ddict_dont_call = True
	# def __getitem__()
# del AttrDict.__call__
import yaml
import os, sys
from path import Path
def rstrip(x,suf):
	if x.endswith(suf):
		x = x[:-len(suf)]
	return x
def _dumps(x):
	return yaml.dump(x)
def _loads(x):
	return yaml.load(x)

_os_stat_result_null = os.stat_result([0 for n in range(os.stat_result.n_sequence_fields)])
def os_stat_safe(fname):
	if os.path.isfile(fname):
		return os.stat(fname)
	else:
		return _os_stat_result_null
