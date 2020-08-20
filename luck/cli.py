#!/usr/bin/env python3

# reopen stdout file descriptor with write mode
# and 0 as the buffer size (unbuffered)
import io, os, sys
# try:
#     # Python 3, open as binary, then wrap in a TextIOWrapper with write-through.
#     sys.stdout = io.TextIOWrapper(open(sys.stdout.fileno(), 'wb', 0), write_through=True)
#     # If flushing on newlines is sufficient, as of 3.7 you can instead just call:
#     # sys.stdout.reconfigure(line_buffering=True)
# except TypeError:
#     # Python 2
#     sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)



import argparse
from luck.header import __version__
import luck.graph

def print_version():
	if '--version' in sys.argv or '-V' in sys.argv:		
	# if args.version == True:
		print(__version__)
		sys.exit(0)
	return 0

def print_help():
	print(f'''
usage: pyluck [-h] subcommand [arguments,...]


Available commands:
  make TARGET          build the specified TARGET. see `pyluck make -h`
  graph [TARGET]	   build the dependency graph for TARGET or all 
                       targets if unspecified

optional arguments:
  -h, --help            show this help message and exit
		'''
		)

	_ = '''
usage: pyluckmake [-h] [-C DIRECTORY] [--abs-target ABS_TARGET] [-f LUCKFILE]
                  [--pdb] [--debug-class DEBUG_CLASS] [-V]
                  target

positional arguments:
  target                the target within the namespace

optional arguments:
  -h, --help            show this help message and exit
  -C DIRECTORY, --directory DIRECTORY
                        Change to DIRECTORY before doing anything.
  --abs-target ABS_TARGET
                        [NotImplemented][TBC] the full url to the target
  -f LUCKFILE, --luckfile LUCKFILE
                        Path to the luckfile to be imported
  --pdb                 run post-mortem pdb
  --debug-class DEBUG_CLASS
                        DEBUG_CLASS format: <CLASS_NAME:str>:<DEBUG_LEVEL:int>
                        possible values for CLASS_NAME:{{BaseRule}}.set
                        class.debug = DEBUG_LEVEL before execution example
                        --debug-class BaseRule:1
  -V, --version         print version

	'''
def luck_main(ns=None):


	print_version()
	# parser,sub = get_parser()
	# args = parser.parse_args()


	index = None
	for i,v in enumerate(sys.argv):
		if i==0: continue
		if not v.startswith('-'): index = i; break

	if '-h' in sys.argv[:index] or '--help' in sys.argv[:index]:
		print_help()
		sys.exit(0)
	if index is None:
		print("Argument not enough %s"%sys.argv)
		print_help()
		sys.exit(1)

	print_version()	
	command = sys.argv[1]
	del sys.argv[1]
	command = {'make':'build'}.get(command,command)
	luck_prog_main(command,None,ns)

def luck_prog_main(command, args=None,ns=None,):
	print_version()
	build_parser = get_parser()[1]
	if args is None:
		# build_parser.prog = build_parser.prog.rsplit(None,1)[0]
		# if command == "graph":
		args = build_parser.parse_args()

	if args.directory is not None:
		os.chdir(args.directory)

	import luck.types
	for x in (args.debug_class or '').split():
		if ':' in x:
			sp = x.split(':')
			name, debug_val = sp[0], int(sp[1]) 
		else:
			name, debug_val = x    , 1
		setattr( getattr(luck.types, name), 'debug', debug_val)

	target  = args.target
	use_pdb = args.pdb


	try:

		ns = ns or get_default_rulenamespace(args.abs_target, args.luckfile) 
		if command == "build":
			if not len(target):
				build_parser.print_help()
				print("error: the following arguments are required: target")
				sys.exit(1)
			else:
				for _target in target:
					ns[_target].build()
		elif command == "graph":
			if not len(target):
				rules = ns.values()
			else:
				rules = [ns[k] for k in target]
			# print(rules)
			# OFNAME = "temp.dot"
			OFNAME = f'{ns._module_file}.dot'
			luck.graph.rules_to_graph( rules, None, OFNAME, "svg")
			print(f'graph: output to {OFNAME}')
		else:
			assert 0
	except Exception as e:
		if use_pdb:	
			import traceback; traceback.print_exc()
			import pdb; pdb.post_mortem()
		else:
			raise
		# luck_build_main(None, ns)
	# else:
	# 	assert 0,sys.argv

def luck_build_main(args=None, ns=None):
	luck_prog_main('build', args, ns)



from luck.types import RuleNameSpace
def get_default_rulenamespace(abs_target, luckfile):
	'''
	luckfile defaults to "LUCKFILE.py"
	'''
	if abs_target is not None:
		raise NotImplementedError
	else:
		if luckfile.endswith('.py'): luckfile = luckfile[:-3]
		sys.path.insert(0,'')
		mod = __import__(luckfile)
		out = []
		for k,v in vars(mod).items():
			if isinstance(v, RuleNameSpace):
				out.append((k,v))
		if len(out) > 1:
			assert 0,[x[0] for x in out]
		else:
			return out[0][1]

		# return getattr(mod, "ns")


# if __name__ == '__main__':
def get_parser(	):
	'''
	Ref: https://gist.github.com/samtorno/4a52f58f1f81615048dd23b2a1da3c07
	'''	
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers()
	subparsers.required = True
	subparsers.dest = 'command'

	# get our global options and subcommand

	# parser.add_argument('--database', help='Specify a database to use (default = ./tickets.db)')
	# parser.add_argument('--service', help='Specify which service to work with')

	# build_parser = subparsers.add_parser('build', help='build a target')
	# build_parser = subparsers.add_parser('make', help='build a target')
	# build_parser = subparsers.add_parser('make', help='build a target')
	build_parser = argparse.ArgumentParser()
	build_parser.add_argument('target', help='the target within the namespace',nargs="*")
	build_parser.add_argument('-C', '--directory', help='Change to DIRECTORY before doing anything.',)
	build_parser.add_argument('--abs-target',help='[NotImplemented][TBC] the full url to the target',
		required=False)
	build_parser.add_argument('-f','--luckfile', default='LUCKFILE.py', help='Path to the luckfile to be imported',)

	build_parser.add_argument('--pdb',help='run post-mortem pdb',
	    default=False, action="store_true")
	build_parser.add_argument('--debug-class',help='DEBUG_CLASS format: <CLASS_NAME:str>:<DEBUG_LEVEL:int> possible values for CLASS_NAME:{{BaseRule}}.'
		'set class.debug = DEBUG_LEVEL before execution\n'
		'example --debug-class BaseRule:1',
	    # default=False, 
	    )

	for p in [parser,build_parser]:
		p.add_argument('-V','--version',help='print version',
	    default=False, action="store_true")
	return parser, build_parser


if __name__ == '__main__':
	luck_main()