import future_fstrings
from attrdict import AttrDict as _AttrDict
from path import Path
import graphviz

__version__ = '0.0.8'
PACKAGE_NAME = 'luck'

def require_version(required_version):
	assert required_version>__version__, f"required a higher verion {required_version} than runtime {__version__}"


class RuleNotDefined(Exception):
	pass

class SetAttrDenied(Exception):
	pass

class AttrDict(_AttrDict):
	_ddict_dont_call = True
	# def __getitem__()
# del AttrDict.__call__

import inspect
def get_frame(frame):
	if frame is None:
		frame = inspect.currentframe().f_back.f_back ####parent of caller by default
	return frame

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

def dir_listfiles(dirName):
	'''
	REF: https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
	'''
	listOfFiles = list()
	for (dirpath, dirnames, filenames) in os.walk(dirName):
		listOfFiles += [os.path.join(dirpath, file) for file in filenames]
	return listOfFiles
