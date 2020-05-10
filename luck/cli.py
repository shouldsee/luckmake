#!/usr/bin/env python3

import sys,os
import argparse
from luck.header import __version__
def print_version():
	if '--version' in sys.argv or '-V' in sys.argv:		
	# if args.version == True:
		print(__version__)
		sys.exit(0)
	return 0
def luck_main(ns=None):
	print_version()
	parser,sub = get_parser()
	args = parser.parse_args()
	# import pdb; pdb.set_trace()
	if args.command == 'build':
		luck_build_main(args, ns)

def luck_build_main(args=None, ns = None):
	print_version()
	if args is None:
		build_parser = get_parser()[1]
		build_parser.prog = build_parser.prog.rsplit(None,1)[0]
		args = build_parser.parse_args()
		# args = get_parser()[1].parse_args()
		# build_parser
	if args.directory is not None:
		os.chdir(args.directory)
	target  = args.target
	use_pdb = args.pdb	
	try:
		import luck.types
		for x in (args.debug_class or '').split():
			if ':' in x:
				sp = x.split(':')
				name, debug_val = sp[0], int(sp[1]) 
			else:
				name, debug_val = x    , 1
			setattr( getattr(luck.types, name), 'debug', debug_val)

		ns = ns or get_default_namespace(args.abs_target) 
		ns[target].build()
	except Exception as e:
		if use_pdb:	
			import traceback; traceback.print_exc()
			import pdb; pdb.post_mortem()
		else:
			raise


def get_default_namespace(abs_target):
	if abs_target is not None:
		raise NotImplementedError
	else:
		sys.path.insert(0,'')
		mod = __import__('LUCKFILE')
		return mod.ns


# if __name__ == '__main__':
def get_parser():
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

	build_parser = subparsers.add_parser('build', help='build a target')
	build_parser.add_argument('target', help='the target within the namespace')
	build_parser.add_argument('-C', '--directory', help='Change to DIRECTORY before doing anything.',)
	build_parser.add_argument('--abs-target',help='[NotImplemented][TBC] the full url to the target',
		required=False)
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