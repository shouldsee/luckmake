
from .header import PACKAGE_NAME, __version__
from .header import AttrDict, Path, dir_listfiles
from .header import SetAttrDenied, RuleNotDefined
from .shell  import FstringShellCommand, get_frame
import inspect
class BuildRuleContext(AttrDict):
	pass


def dns_getitem(k, v,debug = 0):
		if callable(v) and not getattr(v, '_ddict_dont_call', False):
			_v = v()
		else:
			_v = v
		if debug: print(k,_v)
		return _v

class DelayedNameSpace(AttrDict):
	_ddict_dont_call = True
	def __init__(self, *a, **kw):
		self._allow_invalid_attributes = True
		super().__init__(*a, **kw)
	def __setitem__(self,k,v):
		super().__setitem__(k,v)
	def __getattr__(self,k ):
		# if debug: print(f'[getattr]{k!r}{self.__class__!r}')
		return super().__getattr__(k)
	def __getattribute__(self,k ):
		# print(f'[getattribute]{k!r}{type(self)!r}')
		return super().__getattribute__(k)
	def __getitem__(self,k):
		v = super().__getitem__(k)
		return dns_getitem(k, v)

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
	def subclass(cls, name, registry=None, attrs={}, ruleFactory=None, module_file = None):
		v = type( name, (cls,), attrs)
		if registry is not None:
			registry[name] = v
		if ruleFactory is not None:
			v._ruleFactory = ruleFactory
		if module_file is not None:
			v._module_file = module_file
		return v
	def get_raw(self,k):
		return super().__getitem__(k)
	raw = get_raw

DNS = DelayedNameSpace
DNSUB = lambda *a:DelayedNameSpace.subclass(*a)()

class RuleNameSpace(DNS):
	_ruleFactory = None
	_module_file = None
	def __init__(self, *a,**kw):
		# import inspect
		pframe = inspect.currentframe().f_back
		if self._module_file is None:
			self._module_file = pframe.f_locals['__file__']
		# import pdb; pdb.set_trace()
		super().__init__(*a,**kw)
		# self.setdefault('ruleFactory', BaseRule)

	def copy(self):
		raise NotImplementedError
		
		res = type(self)(super().copy())
		for k in res:
			if isinstance(res[k],BaseRule):
				res.attach_rule(res[k])
		return res

	def attach_rule(self, rule, output_name=None):
		'this is a one way attachment'
		rule['namespace'] = self
		# print(f'[attaching]{type(self)!r}{type(rule).__name__}{type(rule)!r}')
		# self.untouched()[rule.output] = True
		super().__setitem__(output_name or rule.output, rule)


	def __setitem__(self, k, v):
		if v is None:
			v = (None,None,None)

		rule_class = None 
		if len(v)>=3: 
			'v[3-1] is the rule_class'
			rule_class = v[3-1]
		if rule_class is None:
			# raise NotImplementedError
			rule_class = BaseRule if self._ruleFactory is None else self._ruleFactory

		for output in k.split():
			rule = rule_class(self, output, *v)

		return 
class TestRuleNameSpace(RuleNameSpace):
	_module_file = "__test__"



import functools
def SetterFromRule(rule_class):
	return rule_class.modify

RNS = RuleNameSpace

def CommandFromRule(rule_class):
	pass

import glob

BLACKLIST = [ f'_{PACKAGE_NAME}', '__pycache__', '_luck']

def str_expand(input, debug=0, blacklist= BLACKLIST):
	_ = '''
	If input contains luck/* and luck/**, should get expanded into existing files and 
	a pointer to non-existing files. The pointer should be resolved at build-time/dag creation time.
	If ouput conatins luck/* and luck/**, do nothing because output should not contain pointer
	'''
	out = []
	for x in input.split():
		if '**' in x:
			pre, suf = x.split('**')
			res = dir_listfiles(pre)
			res = [x for x in res if x.endswith(suf) and all((y not in x for y in blacklist))]
			if debug: print(f'[**]{x}{res}')
		elif '*' in x:
			res = glob.glob(x)
			res = [x for x in res if all((y not in x for y in blacklist))]
			if debug: print(f'[*]{x}{res}')	
		else:
			res = [x]
			if debug: print(f'[*]{x}{res}')	
		out.extend(res)
	out = ' '.join(out)
	return out 

class BaseRule(object):
	__doc__ = '''
	__setattr__ only available fo private attribute. do not setattr!


	'''
	debug = 0
	_ddict_dont_call = True
	_inited = False
	def __init__(self, namespace, output, input=None, recipe= None, rebuilt=None, ):
		if input        is None: input   = ''
		if recipe       is None: recipe  = lambda c:None
		if rebuilt      is None: rebuilt = False
		# self._inited    = False
		self._namespace = namespace
		self._dirname   = Path('.').realpath()
		self._output    = str_expand(output)
		self._input     = str_expand(input)
		self._recipe    = recipe
		self._recipe._ddict_dont_call = True
		self._rebuilt   = rebuilt

		# for name in set([self.output] + self.output.split()):
		for name in self.output.split():
			# print(f'[BaseRule]{name!r}')
			ns = namespace
			assert isinstance(ns, RuleNameSpace), (f'{ns.__class__}')
			ns.attach_rule(self, name)
		self._inited    = True
		
	@classmethod
	def modifyWithFrame(rule_class, namespace, outputs, input=None, recipe=None,rebuilt=None,frame=None):
		from luck.shell  import FstringShellCommand, get_frame
		if type(recipe) is str:  recipe  = FstringShellCommand(recipe,get_frame(frame));		
		return rule_class.modify(namespace, outputs, input, recipe, rebuilt)
	MWF = modifyWithFrame

	@classmethod
	def modify(rule_class, namespace, outputs, input=None, recipe=None,rebuilt=None):
		output = outputs
		rule = rule_class(namespace, output, input, recipe, rebuilt)
		return rule
	M = modify

	def __getitem__(self,k):
		v = self.__getattr__(k)
		return v

	def __getattr__(self,k):
		v = getattr(self,'_%s'%k)
		return dns_getitem(k, v)

	def __setattr__(self,k,v, allowed = False):
		if self._inited:
			if not allowed:
				raise SetAttrDenied(f'__setattr__({k!r}) disabled for {self.__class__!r} after initialisation. Use __setitem__ instead')
		return super().__setattr__(k,v)

	def __setitem__(self,k,v):
		return self.__setattr__("_%s"%k,v, True)

	def __call__(self):
		return self.build()

	def inputs_mattered(self):
		ns = self.namespace
		out = []
		for input in self.input.split():
			if input not in ns.keys():
				raise RuleNotDefined(f'Rule {input!r} not defined for {ns.__class__}')
			out.append(ns[input])
		return out

	def build_inputs(self):
		# inputs = self.input.split()
		# ns = self.namepsace
		for input_mat in self.inputs_mattered():			
			# print('[build_inputs]',input_mat.output, input_mat.check())
			retcode = input_mat.build()
		return 0

	def check_inputs(self):
		ret = True
		for input_mat in self.inputs_mattered():
			# if debug: print(f'[checking]{input_mat.output!r} for {self.output!r}')
			if (input_mat.rebuilt) or (not input_mat.check()):
				ret = False
				break
		return ret

	def check(self):
		_ = '''
		check whether this Rule needs update 
		'''
		return self.check_self() and self.check_inputs() 

	def check_self(self):
		raise NotImplementedError()

	def build_after(self):
		# print(f'[rebuilt]{self.output!r}')
		# self.rebuilt = True
		self['rebuilt'] = True
		return 0

	def build(self, debug=0):
		debug = debug or self.debug
		header = '[BaseRule.build()]'
		self['result'] = None
		if debug: print(
			f'{header} {self.output!r}\t{self.input!r}\t{self.__class__.__name__!r} \n'
			f'{header} check:{self.check():d} rebuilt:{self.rebuilt:d} check_self:{self.check_self():d}| check_inputs:{self.check_inputs():d}'
			)
		if (not self.rebuilt) and (not self.check()):
			# self.build_before()
			if debug: print(f'{header} building {self.output!r}')
			if self.build_inputs()!=0:
				assert 0, f"Unable to build inputs for {self!r}"
			self['result']  = self.recipe( BuildRuleContext(o=self.output.split(), i=self.input.split()))
			self.build_after()

		else:
			if debug: print(f'{header} skipping {self.output!r}')
			pass
		return self

class NoCacheRule(BaseRule):
	def check_self(self): return False

