<a  href="https://travis-ci.com/shouldsee/luck"><img src="https://travis-ci.com/shouldsee/luck.svg?branch=master"><img></a>

# LUCK: LUigi-based Compiling Kit for pdb-debuggable builds.

## Overview:

Makefile is traditional and is great. But makefile can be difficult to debug, interrupt. 
In contrast, pdb module in python allows very easy high-level debugging as compared to gdb.
Since my quick search did not reveal any obvious Python alternative to gnu-make, I decided
to adapt the well-known pipeline manager [**luigi**](https://github.com/spotify/luigi) to 
check and resolve the dependency.

This is so far a personal project that helped me understood how luigi works, but if anyone
find this useful, feel free to write documentation / extension modules and make issues/PR.

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



## install 

### Requires:

- Python >= 3.5 
- a modern version of pip

### install source via pip 

```bash
pip install luck@https://github.com/shouldsee/luck/tarball/master
```

## Example

adapted from ECE264

while `make` looks for Makefile in current directory, `luck` looks for "LUCKFILE.py"

```bash
cd example-ece264-hw04.dir
luck clean
luck testall
echo [FIN]
```

Here is a side by side comparison of Makefile and LUCKFILE.py. 
You would notice that LUCKFILE.py is significantly more verbose, but 
there is definitely space for a more concise grammar. After all,
writing python is not about saving FLOC but about saving documentation/communication.


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