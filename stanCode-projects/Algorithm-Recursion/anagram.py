"""
File: anagram.py
Name: Alan Tsai
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""

import time

# Constants
FILE = 'dictionary.txt'                                 # This is the filename of an English dictionary
EXIT = '-1'                                             # Controls when to stop the loop

# Global Variable
dict_lst = []                                           # list of word dictionary


def main():

    print('Welcome to stanCode "Anagram Generator" (or -1 to quit)')
    read_dictionary()                                   # read file and save to list of dictionary

    # while loop for input
    while True:
        word = input('Find anagrams for: ')             # input word
        if word.strip() == EXIT:                        # end loop condition
            break

        t_2 = time.time()
        find_anagrams(word)                             # to find anagrams
        print(f'Searching time: {time.time()-t_2} s')
        print('')


def read_dictionary():
    """
    :return: list, include all word in FILE
    """
    with open(FILE, 'r') as f:
        for line in f:
            dict_lst.append(line.strip())               # read word by line, and strip space & \n


def find_anagrams(s):
    """
    :param s: string, the word want to find anagrams
    :return: none, print result in this function
    """
    ans_lst = []

    print('Searching..')
    find_anagrams_helper(s, '', ans_lst)
    print(f'{len(ans_lst)} anagrams:  {ans_lst}')


def find_anagrams_helper(s_4c, s_n, ans_lst):
    """
    :param s_4c: string, left string for choose
    :param s_n: string, string now, permutation ch to be word
    :param ans_lst: list, ans list to save what word find already
    :return:
    """
    if len(s_4c) == 0:                                  # base case: when already choose all ch
        # if this is word in dictionary list and not in answer list, pass useless string
        if s_n in dict_lst and s_n not in ans_lst:      # if it's word in dict_list and not found before
            print(f'Found:  {s_n}')                     # print this word
            ans_lst.append(s_n)                         # save to answer list
            print('Searching...')                       # find 1 then searching next one

    else:                                               # recursion: when didn't choose all ch, need choose next one
        # Prune, if this prefix and the length of word are not in the dictionary, return this choose
        if len(s_n) >= 2 and not has_prefix(s_n, len(s_n) + len(s_4c)):
            return

        for i in range(len(s_4c)):                      # for loop to choose 1 ch(in s_4c) add to ans
            # Choose
            s_n += s_4c[i]                              # choose a new ch to string now
            # Explore
            ns_4c = s_4c[:i] + s_4c[i + 1:]             # update new string for choose, which send to next recursion
            find_anagrams_helper(ns_4c, s_n, ans_lst)   # recursion,
            # Un-choose
            s_n = s_n[:len(s_n) - 1]                    # string now pop last ch


def has_prefix(sub_s, len_ans):
    """
    :param sub_s: string, the prefix need to check in dictionary list or not
    :param len_ans: length of answer
    :return:
    """
    for word in dict_lst:
        if len(word) == len_ans:                        # check len first will faster than second
            if word.startswith(sub_s):                  # check word in dictionary has prefix or not
                return True


if __name__ == '__main__':
    main()
