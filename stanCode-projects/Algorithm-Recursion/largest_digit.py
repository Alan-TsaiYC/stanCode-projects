"""
File: largest_digit.py
Name: Alan Tsai
----------------------------------
This file recursively prints the biggest digit in
5 different integers, 12345, 281, 6, -111, -9453
If your implementation is correct, you should see
5, 8, 6, 1, 9 on Console.
"""


def main():
	print(find_largest_digit(12345))      # 5
	print(find_largest_digit(281))        # 8
	print(find_largest_digit(6))          # 6
	print(find_largest_digit(-111))       # 1
	print(find_largest_digit(-9453))      # 9


def find_largest_digit(n):
	"""
	:param n: int, to find the largest digit
	:return: int (digit), largest digit in n
	"""
	if n < 0:									# if n is negative, convert to positive
		n *= -1
	return largest_helper(n, 0)					# recursion and return


def largest_helper(n, max_):
	"""
	:param n: : int (positive), to find the largest digit
	:param max_: int (ones digit), largest ones digit in n
	:return: max_, int (ones digit), largest ones digit in n
	"""
	if n % 10 > max_:					# if last ones digit > max_, replace max_
		max_ = n % 10

	if n//10 == 0:						# base case, when n is ones digit, return max_
		return max_
	else:								# recursion, 12345//10 = 1234
		return largest_helper(n//10, max_)


if __name__ == '__main__':
	main()
