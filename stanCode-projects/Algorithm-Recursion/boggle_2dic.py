"""
File: boggle.py
Name: Alan Tsai
----------------------------------------
Play boggle game
"""

import time
import string

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'
ROW = 4				# rows of ch_map
COL = 4				# columns of ch_map


def main():
	# input_ch_map()

	# 4 test easy
	ch_map = ['fycl', 'iomg', 'oril', 'hjhu']
	print(ch_map)
	for r in range(ROW):
		for c in range(COL):
			print(ch_map[r][c], end=' ')
		print('')
	# 4 test easy
	dic = {}
	read_dictionary(dic)							# read dictionary and save all words as a list
	boggle(ch_map, dic)							# search then print all words in game of boggle


def read_dictionary(dic):
	"""
	:return: dic, dictionary of all length >=4 words ,key:first 4 ch , value:list of words
	"""
	# ch_lst = list(string.ascii_lowercase)
	# for ch1 in ch_lst:
	# 	for ch2 in ch_lst:
	# 		dic[ch1+ch2] = {}

	t_s = time.time()		# 4 test
	with open(FILE, 'r') as f:
		for line in f:
			word = line.strip()
			if len(word) >= 4:
				if word[:2] not in dic:
					dic[word[:2]] = {}

				if word[2:4] in dic[word[:2]]:
					dic[word[:2]][word[2:4]].append(word)
				else:
					dic[word[:2]][word[2:4]] = [word]

	print(f'key:{len(dic)}, load time: {time.time()-t_s} s')		# 4 test
	return dic


def input_ch_map(ch_map):
	"""
	:param ch_map:
	:return:
	"""
	# global ch_map

	for i in range(ROW):							# input by row, loop ROW times
		row = input(f'{i+1} row of letters: ').lower()		# input like: 'a b c d', case insensitive

		for j in range(len(row)):					# for loop by ch to check space
			if j % 2 == 1 and row[j] != ' ':		# always 1 ch 1 space, if not, exit
				print('Illegal input')
				exit()
		row = row.replace(" ", "")					# after check space ok, delete all space in string
		if row.isalpha() and len(row) == COL:		# if it's alpha and number of ch is right
			ch_map.append(row)						# add to list of ch_map as string
		else:										# if not, exit
			print('Illegal input')
			exit()


def boggle(ch_map, dic):

	ans_lst = []
	t_s = time.time()								# 4 test

	for pos in range(ROW*COL):						# for loop every position's ch as prefix
		t_p = time.time()							# 4 test
		boggle_helper('', pos, [], ans_lst, ch_map, dic)		# specify 1 prefix to search by recursion function
		print(f' 	({pos//COL},{pos%COL}){ch_map[pos//COL][pos%COL]}:{round(time.time()-t_p, 2)}s', end='')  # 4 test

	print(f'\nThere are {len(ans_lst)} words in total.', end='')		# print total number of found words
	print(f'		Total searching time: {time.time()-t_s} s')			# 4 test


def boggle_helper(s_n, pos, used_pos, ans_lst, ch_map, dic):
	"""
	:param s_n: string, string now
	:param pos: int, position, row:pos//COL col:pos%COL
	:param used_pos: list, used position
	:param ans_lst: answer list, already found answer
	:param ch_map:
	:param dic:
	:return: update ans_lst
	"""

	row, col = pos // COL, pos % COL				# convert position to row & column

	# set
	s_n += ch_map[row][col]							# add chosen ch to string_now
	used_pos.append(pos)							# add chosen ch's pos to used_pos

	# Prune
	if len(s_n) == 2:
		if s_n not in dic:
			used_pos.pop()								# return used_pos too
			return
	elif len(s_n) == 4:
		if s_n[2:4] not in dic[s_n[:2]]:			# if no prefix is string_now, return this chosen
			used_pos.pop()								# return used_pos too
			return

	# when found word, print it then keep search
	if len(s_n) >= 4 and (s_n in dic[s_n[:2]][s_n[2:4]]) and (s_n not in ans_lst):
		# print if string_now: len>4 & in dictionary & not in used answer
		print(f'\nFound "{s_n}"					', end='')
		ans_lst.append(s_n)							# add this word to ans_lst

	# Choose and Explore
	for r in range(row-1, row+2):					# find new_pos around now_pos by for loop row & col
		for c in range(col-1, col+2):
			n_pos = r*COL + c						# convert row & col to new_position
			# if new_pos is exists & not used_position, recursion by new_pos(new choose)
			if 0 <= r < ROW and 0 <= c < COL and n_pos not in used_pos:
				boggle_helper(s_n, n_pos, used_pos, ans_lst, ch_map, dic)

	# Un-choose
	used_pos.pop()									# before return, pop this new_pos from used_pos


# # useless in dict data structure
# def has_prefix(sub_s, dic):
# 	"""
# 	:param sub_s:
# 	:param dic:
# 	:return:
# 	"""
# 	for word in dic:
# 		if word.startswith(sub_s):  				# check word in dictionary has prefix(sub_s) or not
# 			return True

def has_prefix(sub_s, dic):
	"""
	:param sub_s:
	:param dic:
	:return:
	"""
	for key in dic:
		if key.startswith(sub_s):  				# check word in dictionary has prefix(sub_s) or not
			return True


if __name__ == '__main__':
	main()
