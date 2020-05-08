def Factory(requires, output, command):
	'''
	:param:`requires` is a list of required tasks
	:param:`output`   is a list of outputed targets
	:param:`command`  is a bash command or some other thing

	return: a task constructor
	'''
	pass

WARNING = "-Wall -Wshadow --pedantic -Wno-unused-variable"
ERROR = "-Wvla -Werror"
TESTFALGS = "-DTEST_COUNTCHAR -DTEST_PRINTCOUNTS"

GCC = f"gcc -std=c99 -g {WARNING} {ERROR} {TESTFALGS}"

SRCS = "main.c filechar.c".split()
OBJS = [rstrip(x,'.c')+'.o' for x in SRCS]

test1 = Factory('hw04'.split(),
	None,
	'''
	./hw04 inputs/2016 >output16
	diff output16 expected/expected16
	'''
	)



hw04 = Factory(OBJS, 
	None,
	f'''
	{GCC} {OBJS} -o hw04
	''',
	)