from path import Path
from lsc.logged_shell_command import LoggedShellCommand as lsc
import filecmp
def test_ece264_example():
	with Path('example-ece264-hw04.dir').realpath() as d:
		fn = (d/ 'output2049').touch()
		lsc(['luck clean'])
		assert not fn.isfile()
		lsc(['luck testall'])
		for idx in ['16','17','18','19']:
			out = 'output20%s'%idx
			exp = 'expected/expected%s'%idx
			assert filecmp.cmp(out, exp),(out,exp)
		lsc(['luck clean'])
		from pprint import pprint
		import sys
		# sys.stderr.write(repr(d.listdir()))
		out = sorted(Path('').glob('*'))
		with open('/tmp/list','w') as f:
			pprint(out, f)
	
		exp = [Path('LICENSE'),
		 Path('LUCKFILE.py'),
		 Path('Makefile'),
		 Path('README.md'),
		 Path('__pycache__'),
		 Path('expected'),
		 Path('filechar.c'),
		 Path('inputs'),
		 Path('main.c'),
		 Path('out.txt')]
		
		assert out==exp,pprint([out,exp])


	# lsc(['bash ./example-ece264-hw04.sh'])


