
if 1:

	import os,sys
	import warnings
	import yaml
	from lsc.logged_shell_command import LoggedShellCommand
	from lsc.logged_shell_command import LoggedShellCommand as lsc
	import luigi
	import luigi.task

	def rstrip(x,suf):
		if x.endswith(suf):
			x = x[:-len(suf)]
		return x


# import pdb; pdb.set_trace()
# from spiper.types import LoggedShellCommand



	_os_stat_result_null = os.stat_result([0 for n in range(os.stat_result.n_sequence_fields)])
	def os_stat_safe(fname):
		if os.path.isfile(fname):
			return os.stat(fname)
		else:
			return _os_stat_result_null

	def _dumps(x):
		return yaml.dump(x)
	def _loads(x):
		return yaml.load(x)

	x= {1:{2:{3:[4,5,{6:None}]}}}
	assert _loads(_dumps(x)) ==x
		# return 
	from path import Path
	def IdentFile(dir_layout, fn, suffix):
		fn = Path(fn)
		if dir_layout == 'clean':
			lst = [fn.dirname()+'/_spiper/'+ fn.basename(),suffix]
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


	class TStampedLocalTarget(luigi.LocalTarget, str):
		def __str__(self):
			return self.path
		# def timestamp
		def to_ident(self,):
			stat = os_stat_safe(self.path)
			res = (self.path, stat.st_mtime, stat.st_size)
			return res
		@property
		def ident_path(self):
			ident_file = IdentFile('flat', self.path, 'ident_yaml')
			return ident_file
		def load_ident(self,):
			loaded = ''
			if self.ident_path.exists():
				with open( self.ident_path,'r') as f:
					loaded = f.read()
			return loaded

		def ident_same(self):
			current = _dumps( self.to_ident() )
			loaded = self.load_ident()

			# print(self.path)
			# print(current)
			# print(loaded)
			# import pdb; pdb.set_trace()
			return current == loaded

		def ident_update(self):
			with open(self.ident_path, 'wb') as f:
				f.write(_dumps(self.to_ident()).encode())
			return 0


		def exists(self):
			path = self.path
			if '*' in path or '?' in path or '[' in path or '{' in path:
				logger.warning("Using wildcards in path %s might lead to processing of an incomplete dataset; "
							   "override exists() to suppress the warning.", path)		
			
			if self.ident_same():
				return True
			else:
				return False
			# self.load_ident()

			return self.fs.exists(path)




	class LinkedTask(luigi.Task):
		'''
		The task is complete only if upstream is completed
		'''
		def complete(self):
			"""
			If the task has any outputs, return ``True`` if all outputs exist.
			Otherwise, return ``False``.

			However, you may freely override this method with custom logic.
			"""
			outputs = luigi.task.flatten(self.output())
			requires = luigi.task.flatten(self.requires())
			vals = [x.exists() for x in outputs] + [x.complete() for x in requires]
			return all(vals or [False])
			# return all( or [False]) and all([x.complete() for x in requires] or [False])
			# map(lambda task:task.complete(), requires), False)

		def run_body(self):
			raise NotImplementedError(self.__class__)
		def run(self):
			self.run_body()
			outputs = luigi.task.flatten(self.output())
			[getattr(x,'ident_update',lambda x:None)() for x in outputs]
			super().run()



	class ExternalFileTask(LinkedTask):
		fn = luigi.Parameter()
		def output(self): return TStampedLocalTarget(self.fn)
		def run_body(self):
			return 0
			# super().run(); 
			if not self.complete(): 
				# pdb.set_trace();
				import pdb; pdb.set_trace()