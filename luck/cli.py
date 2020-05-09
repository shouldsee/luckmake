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
	build_parser.add_argument('--abs-target',help='the full url to the target',
		required=False)
	build_parser.add_argument('--pdb',help='run post-mortem pdb',
	    default=False, action="store_true")
	for p in [parser,build_parser]:
		p.add_argument('-V','--version',help='print version',
	    default=False, action="store_true")
	return parser, build_parser


	# # setup download
	# download_parser = subparsers.add_parser('download', help='Download all tickets from specified service')
	# download_parser.add_argument('-j', '--json', help='Specify a json cache')

	# # setup export
	# export_parser = subparsers.add_parser('export', help='Export all tickets to specified file')
	# export_parser.add_argument('-o', '--output', help='Specify output file',
	# 											 required=True)
	# return parser
	# args = parser.parse_args()

	# # call the command with our args
	# ret = getattr(sys.modules[__name__], 'main_{0}'.format(args.command))(args)
	# sys.exit(ret)

	# main()
if __name__ == '__main__':
	luck_main()