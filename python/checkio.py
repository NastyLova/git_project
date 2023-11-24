def checkio(numbers_array):
	for i in x:
		for j in range(len(x) - 1):
			if abs(x[j]) > abs(x[j+1]):
				y = x[j + 1]
				x[j+1] = x[j]
				x[j] = y
	return x


def fizzbuzz(n):
	if (n % 3) == 0 and (n % 5) == 0:
		return('Fizz Buzz')
	elif (n % 3) == 0:
		return('Fizz')
	elif (n % 5) == 0:
		return('Buzz')
	else:
		return(str(n))
