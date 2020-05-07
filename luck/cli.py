#!/usr/bin/env python3
import sys,os
from lsc.logged_shell_command import LoggedShellCommand as lsc
from lsc.logged_shell_command import list_flatten_strict
# LoggedShellCommand as lsc
from luigi.cmdline import luigi_run
def main():
	if '--help' in sys.argv:
		argv = 'luigi --help'.split()
		# print(lsc('luigi --help'.split()))
	elif '--help-all' in sys.argv:
		argv = 'luigi --help-all'.split()
	else:
		sys.path.insert(0, os.path.realpath( os.getcwd()))
		import LUCKFILE 
		argv = 'luigi --local-scheduler --module LUCKFILE'.split()+sys.argv[1:]
		# argv = ['luigi --local-scheduler --module LUCKFILE',sys.argv[1:],'2>&1']
		# suc,stdout,stderr,logfile = lsc(['luigi --local-scheduler --module LUCKFILE',sys.argv[1:],'2>&1'],check=False)
		# print('[stdout]')
		# print(stdout)
		# print('[stderr]')
		# print(stderr)
		# assert suc, 'See stdout and stderr above'
	# assert 0
	luigi_run(list_flatten_strict(argv)[1:])

if __name__ =='__main__':
	main()