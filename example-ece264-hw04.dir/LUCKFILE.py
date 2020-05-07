from luck.types import ExternalFileTask, LinkedTask, TStampedLocalTarget, LoggedShellCommand, rstrip


WARNING = "-Wall -Wshadow --pedantic -Wno-unused-variable"
ERROR = "-Wvla -Werror"
TESTFALGS = "-DTEST_COUNTCHAR -DTEST_PRINTCOUNTS"

GCC = "gcc -std=c99 -g {WARNING} {ERROR} {TESTFALGS}".format(**locals())

SRCS = "main.c filechar.c".split()
OBJS = [rstrip(x,'.c')+'.o' for x in SRCS]




class hw04(LinkedTask):
	requires = lambda self: [ExternalFileTask('main.c'),ExternalFileTask('filechar.c')]
	output   = lambda self: TStampedLocalTarget('hw04')
	def run(self): 
		LoggedShellCommand([GCC,   [x.path for x in self.input()], '-o', self.output().path]); 
		super().run()


class test1(LinkedTask):
	requires = lambda self: [hw04()]
	output = lambda self: TStampedLocalTarget('output2016.passed')
	def run(self):
		LoggedShellCommand(['./'+self.input()[0].path, 'inputs/2016 > output2016','&&','diff','expected/expected16','output2016'])		
		super().run()


class test2(LinkedTask):
	requires = lambda self: [hw04()]
	output = lambda self: TStampedLocalTarget('output2017.passed')
	def run(self):
		LoggedShellCommand(['./'+self.input()[0].path, 'inputs/2017 > output2017','&&','diff','expected/expected17','output2017'])		
		super().run()

class test3(LinkedTask):
	requires = lambda self: [hw04()]
	output = lambda self: TStampedLocalTarget('output2018.passed')
	def run(self):
		LoggedShellCommand(['./'+self.input()[0].path, 'inputs/2018 > output2018','&&','diff','expected/expected18','output2018'])		
		super().run()


class test4(LinkedTask):
	requires = lambda self: [hw04()]
	output = lambda self: TStampedLocalTarget('output2019.passed')
	def run(self):
		LoggedShellCommand(['./'+self.input()[0].path, 'inputs/2019 > output2019','&&','diff','expected/expected19','output2019'])		
		super().run()


class testall(LinkedTask):
	def requires(self):return [ script(), test1(),test2(),test3(), test4()]

class clean(LinkedTask):
	def run(self):
		LoggedShellCommand('rm -f hw04 *.o output* *.ident_yaml'.split())
		super().run()


# class script(LinkedTask):
# 	def output(self): return TStampedLocalTarget('MAKE.py')
# 	def run(self):
# 		super().run()
