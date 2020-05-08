

WARNING = -Wall -Wshadow --pedantic -Wno-unused-variable
ERROR = -Wvla -Werror
GCC = gcc -std=c99 -g $(WARNING) $(ERROR) 

TESTFALGS = -DTEST_COUNTCHAR -DTEST_PRINTCOUNTS

SRCS = main.c filechar.c
OBJS = $(SRCS:%.c=%.o)

test1: hw04
	./hw04 inputs/2016 > output16
	diff output16 expected/
	
hw04: $(OBJS) 
	$(GCC) $(TESTFALGS) $(OBJS) -o hw04

