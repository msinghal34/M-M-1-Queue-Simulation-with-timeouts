import random
import time
def foo1():
	print(time.time())
	x = random.Random()
	count = 100000000
	for i in range(count):
		count -= 1
	y = random.Random()
	print(time.time())
	print(x.random())
	print(y.random())
	print(x.random())
	print(y.random())
	print(count)
	x = random.getstate()
	# random.seed(10)
	y = random.getstate()
	for i, a in enumerate(list(x[1])):
		for j, b in enumerate(list(y[1])):
			if (a == b):
				print(i,j,a,b)
def foo2():
	print(random.random())
	print(random.random())
	random.seed(2)
	print(random.getstate())

# random.seed(1)
# print(random.random())
# print(random.random())
# print(random.random())
# random.seed(2)
# print(random.random())
# random.seed(0)
# print(random.random())

foo1()
# print(random.random())
# foo2()
# print(random.random())