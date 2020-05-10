pointer.foo:
	touch pointer.foo

result.bar: *.foo
	cat pointer.foo > $@

clean:
	rm -f *.foo *.bar *.c
