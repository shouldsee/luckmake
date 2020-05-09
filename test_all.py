from path import Path
from lsc.logged_shell_command import LoggedShellCommand as lsc
import filecmp
import os

	
def test_testall():
	with (Path(__file__).realpath().dirname()/'example-ece264-hw04.dir') as d:
		import sys; sys.path.insert(0,''); import importlib; import LUCKFILE; importlib.reload(LUCKFILE); from LUCKFILE import ns
		ns['testall'].build()

def test_ece264_example():
	# assert 0,(os.getcwd())
	with (Path(__file__).realpath().dirname()/'example-ece264-hw04.dir') as d:
		# with Path('example-ece264-hw04.dir').realpath() as d:
		fn = (d/ 'main.o').touch()
		lsc(['pyluckbd clean'])
		# print('[cwd]',os.getcwd()
		assert not fn.isfile()
		lsc(['pyluckbd testall'])
		for idx in ['16','17','18','19']:
			out = 'output%s'%idx
			exp = 'expected/expected%s'%idx
			assert filecmp.cmp(out, exp),(out,exp)
		lsc(['pyluckbd clean'])
		from pprint import pprint
		import sys
		# sys.stderr.write(repr(d.listdir()))
		out = sorted(Path('').glob('*'))
		with open('/tmp/list','w') as f:
			pprint(out, f)
		exp = \
[Path('LICENSE'),
  Path('LUCKFILE.py'),
  Path('Makefile'),
  Path('README-example.py'),
  Path('README.md'),
  Path('__pycache__'),
  Path('_luck'),
  Path('expected'),
  Path('filechar.c'),
  Path('inputs'),
  Path('luck'),
  Path('main.c'),
  Path('out.txt'),
  Path('output2049'),
  Path('v1.LUCKFILE.py'),
  Path('LUCKFILE_syntax_A.py'),
  Path('LUCKFILE_syntax_M.py'),
  # Path('new.LUCKFILE.py'),

  # Path('v1E.LUCKFILE.py')
  ]
		exp = sorted(exp)
		out = sorted(out)

		
		assert out==exp,pprint([out,exp])


def test_defer_rulenamespace_setitem():
	from luck.defer import RuleNameSpace as RNS
	from luck.types import NoCacheRule
	ns = RNS()
	ns['clean'] = (None, 
		lambda c: LSC('''
			rm -f hw04 *.o *.ident_yaml output??
			'''), NoCacheRule)
	assert isinstance(ns['clean'],NoCacheRule)

	# lsc(['bash ./example-ece264-hw04.sh'])


