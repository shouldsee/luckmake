<a  href="https://travis-ci.com/shouldsee/luck"><img src="https://travis-ci.com/shouldsee/luck.svg?branch=master"><img></a>

# LUCK: the LUcky Compiling Kit for pdb-debuggable builds.

## install 

### Requires:

- Python >= 3.5 
- a modern version of pip

### install source via pip 

```bash
pip install luck@https://github.com/shouldsee/luck/tarball/master
```

[TBC] compile binaries

## Documentation

[TBC]

## Overview:

### Motivation

Makefile is concise and robust, but can be hard to learn for non-experienced bash user, 
due to its many unique operators. Since python is a much wider spread language than
Makefile (need ref), porting Makefile syntax to Python would open up access to 
make-powered reproducibility to these python-only users, without having to learn
the syntax. 

There are several dimensions to score a build system:

1. learning cost: subjective and scenario-dependent
    - Makefile:    easier for a bash user. less tutorial 
    - LUCKFILE.py: no tutorial yet, only example available. easy for a python user
2. coarseness: high-level or low-level
    - Makefile:    dag level
    - LUCKFILE.py: dag 
3. interface:    cli? gui? web? diagnostic tools? easy to debug?
    - Makefile:    many tools exist for static analysis. [gmd](https://www.cmcrossroads.com/article/dynamic-breakpoints-gnu-make-debugger) for [debugging](https://stackoverflow.com/a/26290571) (yet to try)
    - LUCKFILE.py: simple cli only for now. pdb for debugging `import pdb;pdb.set_trace()`
4. speed: for constructing dag and execution
    - Makefile:    should be faster as is clang, multiprocessed
    - LUCKFILE.py: single-process for now.
5. persistence: whether result is saved to disk, and how easy to enter a corrupted state
    - Makefile:    save mtime for persistence 
    - LUCKFILE.py: use mtime+size or md5sum 
6. portability: easy to install? backend for different platform?
    - Makefile:    `sudo apt install make`
    - LUCKFILE.py: `pip install luck@https://github.com/shouldsee/luck/tarball/master`0
7. extensibility: how easy to write a plugin?
    - Makefile:    possible embedded Scheme (.scm ) (need to learn LISP aside from Makefile)
    - LUCKFILE.py: write python class/callable to inject dependency, same lang as LUCKFILE.py
8. relative or absolute path:
    - Makefile:    NA
    - LUCKFILE.py: NA

## Sciprting Syntax

```

namespace utility
=======================
RNS:    RuleNameSpace
DNSUB:  DelayedNameSpaceSUBclass
LSC:    LoggedShellCommand

callable to execute during build time
======================================
pyfunc: 
AutoCmd:
MFP:    MakeFilePattern: 

rule classes
=========================
BaseRule:
TimeSizeStampRule:
MD5StampRule:
NoCacheRule:
```

## Example

adapted from ECE264

while `make` looks for Makefile in current directory, `luck` looks for "LUCKFILE.py"

```bash
cd example-ece264-hw04.dir
make clean
make testall

luck-build clean
luck-build testall
echo [FIN]
```

### charcount

```
1860 example-ece264-hw04.dir/LUCKFILE.py
2671 example-ece264-hw04.dir/v1.LUCKFILE.py
 895 example-ece264-hw04.dir/Makefile
5426 total
```

Here is a side by side comparison of Makefile and LUCKFILE.py. 
You would notice that LUCKFILE.py is significantly more verbose and have more quotes, but 
there is definitely space for a more concise grammar. 


[./example-ece264-hw04.dir/Makefile](./example-ece264-hw04.dir/Makefile)

```Makefile
WARNING = -Wall -Wshadow --pedantic -Wno-unused-variable
ERROR = -Wvla -Werror
GCC = gcc -std=c99 -g $(WARNING) $(ERROR) 

TESTFALGS = -DTEST_COUNTCHAR -DTEST_PRINTCOUNTS

SRCS = main.c filechar.c
OBJS = $(SRCS:%.c=%.o)

hw04: $(OBJS) 
	$(GCC) $(TESTFALGS) $(OBJS) -o hw04

test1: hw04
	./hw04 inputs/2016 > output16
	diff output16 expected/

```

[./example-ece264-hw04.dir/LUCKFILE.py](./example-ece264-hw04.dir/LUCKFILE.py)

```python
#-*- coding: future_fstrings -*- 
from luck.types import *
## create RuleNameSpace and set default
ns = RNS.subclass('MainRNS')(ruleFactory=TimeSizeStampRule) 
## create patterns namespace 
patterns = DNSUB('PatternNS')

WARNING = "-Wall -Wshadow --pedantic -Wno-unused-variable"
ERROR = "-Wvla -Werror"
TESTFALGS = "-DTEST_COUNTCHAR -DTEST_PRINTCOUNTS"

GCC = f"gcc -std=c99 -g {WARNING} {ERROR} {TESTFALGS}"

SRCS = "main.c filechar.c"
OBJS = ' '.join([x[:-2]+'.o' for x in SRCS.split()]) ## pure python func!
ns[OBJS] = (SRCS, AutoCmd(patterns))
ns[SRCS] = (None,None, TimeSizeStampRule)

patterns[0] = MakefilePattern(
	'%.o','%.c', 
	lambda x: LSC(f'{GCC} {TESTFALGS} -c {x.inputs[0]} -o {x.outputs[0]}'))

ns['./hw04'] = (f'{OBJS}',
	lambda c:LSC(f'''
		{GCC} {TESTFALGS} {OBJS} -o {c.o[0]}
		'''))
### c.i, c.o instead of $< $@
ns['test1'] = ('./hw04', lambda c:LSC(f'''
	{c.i[0]} inputs/2016 > output16
	diff output16 expected/expected16
	echo [passed] test1
	'''))

if __name__ == '__main__':
	from luck.cli import luck_main
	luck_main(ns)
```

[./example-ece264-hw04.dir/v1.LUCKFILE.py](./example-ece264-hw04.dir/v1.LUCKFILE.py) *Older version*

```python
from luck.types import ExternalFileTask, LinkedTask, TStampedLocalTarget, LoggedShellCommand, rstrip
# or just import *

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
		LoggedShellCommand([GCC, [x.path for x in self.input()], '-o', self.output().path]); 
		super().run()


class test1(LinkedTask):
	requires = lambda self: [hw04()]
	output = lambda self: TStampedLocalTarget('output2016.passed')
	def run(self):
		LoggedShellCommand(['./'+self.input()[0].path, 'inputs/2016 > output2016','&&','diff','expected/expected16','output2016'])		
		super().run()
```

## Improvements:

- [urg,perf] multi-worker build.. preferably a portable implementation
- [urg,urg] shall I use f-string?
- [sug,urg] get rid of `super().run()` for subclasses of LinkedTask
- [sug] adding utility function for gdb upon exception
- [sug] use "self.input().path" or "self.input()" ?
- [doc] Add docs/
- [port] Python is not the best language for writing a build system because of its poor portability.
I am using python because it is more expressive than a static yaml/json file. It would be 
great if we can write a parser in c/cpp/go to emulate a reduced version of python.
- [sug] profiling gprof
- [sug,ada] dry run dependency graph

### in-depth comparison

[TBC]


### Alternatives and Refs

- https://medium.com/@mattia512maldini/looking-for-a-makefile-alternative-6e7f795b5cad
- https://alternativeto.net/software/gnu-make/
- {name}: {stars}k, {comments}
- go / python
- go-task: 1.7k go (liked)
- luigi: 13k, python (included, no DSL)
- joblib: 2k, python  (persistent cache)
- scons: 0.8k, python (DSL, high-level)
- snakemake: 0.5k, python (similar, but use DSL)
- galaxy: 0.7k python (use-xml)
- waf: 0.078k, python
- sake: 0.3k, python
- redo: 1.4k, python (use-bash)
- java / groovy 
- gradle: 10.5k, groovy maybe? see bazel
- maven: 2.1k, na,  xml-based
- buck: 7.3k, java android-spec
- c / cpp
- cmake: na, cpp?
- gnumake: na, no
- premake: 1.6K, clang
- makeme: 0.02k, clang
- ninja build: 5.5k, c or cpp
- other
- ant: na, xml
- rake: na, ruby, maybe
- sbt: na, java/scala, maybe
- not-compared
- apache-airflow: too big
