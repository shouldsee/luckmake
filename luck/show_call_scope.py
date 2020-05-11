import fstr
import decimal

# fmt = "result: {value:{width}.{precision}}"

# x = fstr(fmt)


def f1():
	print(x)

def f2():
	print( f'{x}')

def make_f3():
	import inspect
	f_back = inspect.currentframe().f_back
	f3 = eval('lambda: print(f"{x}")',f_back.f_locals, f_back.f_globals)
	return f3

f3 = make_f3()
def main():
	x = 123
	f1()
	f2()
	f3()

x = 123
main()

