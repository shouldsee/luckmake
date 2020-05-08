#-*- coding: future_fstrings -*- 
from .header import AttrDict, RuleNotDefined
class BuildRuleContext(AttrDict):
	pass

class DelayedNameSpace(AttrDict):
	def __init__(self, *a, **kw):
		self._allow_invalid_attributes = True
		super().__init__(*a, **kw)
	def __setitem__(self,k,v):
		super().__setitem__(k,v)
	def __getitem__(self,k):
		debug  = 0
		v = self.get_raw(k)
		if callable(v) and not getattr(v, '_ddict_dont_call', False):
			_v = v()
		else:
			_v = v
		if debug: print(self,k,_v)
		# if _v ==0:
		# 	import pdb; pdb.set_trace()
		return _v
			# if debug: print(self,k,v)
			# return v
	def copy(self):
		return type(self)(super().copy())
	def fix_within_context(self, context=None, copy=True):
		'''
		Materialise all callable unless marked by _ddict_dont_call
		'''
		debug = 0
		if copy:
			out = self.copy()
		else:
			out = self
		for k in self:
			out[k] = self[k]
			if debug: print(f'[{self.__class__.__name__},{k}],{self[k]}')
		return out
	fiwic = fix_within_context

		# for k in 
	@classmethod
	def subclass(cls, name, registry=None, attrs={}):
		v = type( name, (cls,), attrs)
		if registry is not None:
			registry[name] = v
		return v
	def get_raw(self,k):
		return super().__getitem__(k)
DNS = DelayedNameSpace
DNSUB = lambda *a:DelayedNameSpace.subclass(*a)()

class RuleNameSpace(DNS):
	def __init__(self,*a,**kw):
	    super().__init__(*a,**kw)
	    self.setdefault('ruleFactory', BaseRule)

	def copy(self):
		res = type(self)(super().copy())
		for k in res:
			res.attach_rule(res[k])
		return res
	def attach_rule(self, rule):
		'this is a one way attachment'
		rule.namespace = self
		# self.untouched()[rule.output] = True
		super().__setitem__(rule.output, rule)

	def add_rule(self, outputs, input, recipe, rule_class = None):
		'''
		Materialised Rules using a factory
		'''
		if input is None:
			input = ''
		if outputs is None:
			assert 0
		if recipe is None:
			recipe = lambda c:None		
		if rule_class is None:
			rule_class = self.ruleFactory

		for output in outputs.split():
			rule = rule_class(output=output, input=input, recipe=recipe)
			self.attach_rule(rule)
			# rule = self._init_rule(output, input, recipe, rule_class)

	def __setitem__(self, k, v):
		if v is None:
			v = (None,None,None)
		self.add_rule(k, *v)
		return 


class BaseRule(DelayedNameSpace):
# class BaseRule():
	_ddict_dont_call = True
	def __init__(self,*a,**kw):
		super().__init__(*a,**kw)
		self.setdefault('namespace',None)
		self.setdefault('rebuilt', False)

		self.setdefault('input',None)
		self.setdefault('output',None)
		self.setdefault('recipe',None)
		# if self.recipe is not None:
		self.get_raw("recipe")._ddict_dont_call = True

	def __call__(self):
		return self.build()

	def inputs_mattered(self):
		ns = self.get_raw('namespace')
		out = []
		for input in self.input.split():
			if input not in ns.keys():
				raise RuleNotDefined(f'Rule {input!r} not defined for {ns.__class__}')
			out.append(ns[input])
		return out

	def build_inputs(self):
		# inputs = self.input.split()
		ns = self.get_raw('namespace')
		for input_mat in self.inputs_mattered():			
			# print('[build_inputs]',input_mat.output, input_mat.check())
			retcode = input_mat.build()
		return 0

	def check_inputs(self):
		ret = True
		for input_mat in self.inputs_mattered():
			if not input_mat.check():
				ret = False
				break
		return ret

	def check(self):
		_ = '''
		check whether this Rule needs update 
		'''
		return (not self['rebuilt']) and self.check_self() and self.check_inputs() 

	def check_self(self):
		raise NotImplementedError()

	def build_after(self):
		# print(f'[rebuilt]{self.output!r}')
		self['rebuilt'] = True
		return 0

	def build(self):
		self.res = None
		if not self.check():
			# self.build_before()
			if self.build_inputs()!=0:
				assert 0, f"Unable to build inputs for {self!r}"
			recipe = self.get_raw('recipe')
			self.res  = recipe( BuildRuleContext(o=self.output.split(), i=self.input.split()))

			self.build_after()

		else:
			pass
		return self

class NoCacheRule(BaseRule):
	def check_self(self): return False

