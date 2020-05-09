#-*- coding: future_fstrings -*- 
from .header import AttrDict


class MakefilePattern(object):
	'''
	[TODO] Only support sinlge output target
	'''

	def __init__(self, output_ptn, input_ptn, recipe=None):
		# if recipe is None:
		# 	recipe = input_ptn
		# 	output_ptn, input_ptn = output_ptn.split(':')
		if recipe is None: recipe = lambda c:None

		self.output_ptn = output_ptn.strip().split('%')
		self.input_ptn_list  = [input_ptn.strip().split('%') for input_ptn in input_ptn.split()]
		self.recipe       = recipe
		for x in self.input_ptn_list:
			assert len(x)==2,(input_ptn)
		# assert len(self.input_ptn)==2,input_ptn
		assert len(self.output_ptn) == 2,output_ptn
	@classmethod
	def modify(cls, namespace, key, output_ptn, input_ptn, recipe=None):
		namespace[key] = v =cls(output_ptn, input_ptn, recipe)	
		return v
	M = modify

	def match(self, output, inputs):
		'''
		[TODO] use original gnu-make code for this recipetion?
		'''
		# inputs = 
		# for input in inputs:
		debug = 0
		if debug: print(self.output_ptn, self.input_ptn_list)
		if debug: print (output,':',inputs)
		def _matched(x,x_ptn):
			res = x.startswith(x_ptn[0]) and x.endswith(x_ptn[1])
			if debug: print(x,x_ptn,res)
			return res
		def _extract_stem(x,x_ptn):
			pre,suf = x_ptn
			return x[len(pre):-len(suf)]

		matched_input = []
		if not _matched(output, self.output_ptn):
			return matched_input
		else:
			stem = _extract_stem(output, self.output_ptn)
			for _input_ptn in self.input_ptn_list:
				_pre, _suf = _input_ptn
				require = f'{_pre}{stem}{_suf}'
				if not require in inputs:
					_ = f'Cannot find {require!r} in {inputs!r}, Aborting match'
					abort = True
					break
				else:
					matched_input.append(require)
			return matched_input

			# if self.input_ptn

		return True
	def __call__(self, *a,**kw):
		return self.build(*a,**kw)
	def build(self, outputs, inputs, rule_outputs, rule_inputs):
		self.res = self.recipe(AttrDict(
			o=outputs, i=inputs,
			outputs = outputs, inputs=inputs,
			pattern_outputs=outputs,   pattern_inputs=inputs, 
			rule_outputs=rule_outputs, rule_inputs=rule_inputs))
		return self
			# inputs)
		# inputs, outputs)


class AutoCmd(object):
	_ddict_dont_call = True
	def __init__(self, rules):
		self.rules = rules

	# def __call__(self, outputs, inputs):
	def __call__(self, *a, **kw):
		return self.build(*a,**kw)

	def build(self, c):
		outputs = c.o
		inputs  = c.i
		# _= 'find a match for output as a whole'
		_= 'find a match for each output on its own'
		matched_by_output = []
		for output in outputs:
			matched = []
			for key, rule in self.rules.items():
				match_input = rule.match(output,inputs)
				if match_input:
					matched.append((output, match_input,rule, key ))
			matched_by_output.append( matched )


		matched_by_output_checked = out = []
		for matched in matched_by_output:
			assert len(matched)==1,(output, matched)
			_ = '[TODO] add more message'
			out.append(matched[0])

		for (matched_output,matched_inputs, rule, key) in matched_by_output_checked:
			rule.build( [matched_output], matched_inputs, outputs, inputs)
		return 0
