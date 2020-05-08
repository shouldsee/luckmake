#!/usr/bin/env python3

import sys,os
import argparse

def luck_main(ns=None):
	parser,sub = get_parser()
	args = parser.parse_args()
	# import pdb; pdb.set_trace()
	if args.command == 'build':
		luck_build_main(args, ns)

def luck_build_main(args=None, ns = None):
	if args is None:
		args = get_parser()[1].parse_args()
		# build_parser
	target = args.target
	ns = ns or get_default_namespace(args.abs_target) 
	ns[target].build()


def get_default_namespace(abs_target):
	if abs_target is not None:
		raise NotImplementedError
	else:
		sys.path.insert(0,'')
		import LUCKFILE
		return LUCKFILE.ns


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
	build_parser.add_argument('--abs-target',help='the full url to the target',
		required=False)

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