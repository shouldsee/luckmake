

from .header import Path, PACKAGE_NAME, __version__
from .header import (_dumps,_loads,os_stat_safe)
from .defer import BaseRule
from collections import OrderedDict

def IdentFile(dir_layout, fn, suffix):
	fn = Path(fn)
	if dir_layout == 'clean':
		lst = [fn.dirname()+'/_%s/'%PACKAGE_NAME+ fn.basename(),suffix]
		# job_name, suffix]
		# input_ident_file = '{pre_dir}/_spiper/{pre_base}.{job_name}.{suffix}'.format(**locals())
	elif dir_layout == 'flat':
		lst = [fn,suffix]
		# lst = [fn,job_name,suffix]
	else:
		assert 0,("dir_layout",dir_layout)
		# input_ident_file = '{prefix}.{job_name}.{suffix}'.format(**locals())
	input_ident_file = '.'.join(lst)
	return Path(input_ident_file)


class StampRule(BaseRule):
	_ddict_dont_call = True
	layout = 'clean'
	def check_self(self):
		if self.ident_same():
			return True
		else:
			return False
	def build_after(self):
		self.ident_update()
		return super().build_after()

	# @property
	def ident_path(self):
		ident_path = IdentFile(self.layout, Path(self.output).realpath(), 'stamp_yaml')
		ident_path.dirname().makedirs_p()
		return ident_path

	def load_ident(self,):
		loaded = ''
		if self.ident_path().exists():
			with open( self.ident_path(),'r') as f:
				loaded = f.read()
		return loaded

	def to_ident_call(self):
		to_ident = self.to_ident(self.output, self.input, self.recipe)
		ident = ([
			# [f'__version__: {__version__}'],
			('__version__',__version__),
			('__class__.__name__',self.__class__.__name__),
			('to_ident', list(to_ident)),
			])
		ident = [list(x) for x in ident]
		return ident

	def ident_same(self):
		ident = self.to_ident_call()
		# self.to_ident(self.output, self.input, self.recipe) 
		current = _dumps( ident)
		loaded = self.load_ident()
		return current == loaded

	def ident_update(self):
		with open(self.ident_path(), 'wb') as f:
			f.write(_dumps(self.to_ident_call()).encode())
		return 0



class TimeSizeStampRule(StampRule):

	@staticmethod
	def to_ident(output, input, recipe):
		stat = os_stat_safe(output)
		res = (output, stat.st_mtime, stat.st_size)
		return res


import hashlib
from functools import partial
import os

def safe_md5sum(filename):
	if os.path.isfile(filename):
		return md5sum(filename)
	else:
		return -1

def md5sum(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()

class MD5StampRule(StampRule):
	@staticmethod
	def to_ident(output, input, recipe):
		res = [
			['output',output],
			['safe_md5sum',safe_md5sum(output)],
		]
		return res
