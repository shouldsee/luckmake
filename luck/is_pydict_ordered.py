import random
from pprint import pprint
for i in range(100):
	x = [(random.random(),random.random()) for i in range(10)]
	# d = dict(d)
	y = list(dict(x).items())
	assert y==x,pprint(list(zip(x,y)))
	# print(d)
	# break
	# random.random(10)