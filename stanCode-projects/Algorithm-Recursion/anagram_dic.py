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
dic = {}                                                # list of word dictionary


def main():
    print('Welcome to stanCode "Anagram Generator" (or -1 to quit)')

    t_s = time.time()
    read_dictionary()                                   # read file and save to dic (dictionary)
    print(f'File load time: {time.time()-t_s} s')

    while True:                                         # while loop for input
        word = input('Find anagrams for: ')             # input word
        if word.strip() == EXIT:                        # end loop condition
            break

        t_2 = time.time()
        find_anagrams(word)                             # to find anagrams
        print(f'Searching time: {time.time()-t_2} s')
        print('')


def read_dictionary():
    """
    :return: none, update dict = {'ab' : ['ab', 'ba'] , 'abc' : ['abc', 'bac', 'cab']}
    """
    with open(FILE, 'r') as f:
        for line in f:
            word = line.strip()
            sorted_ch = sort_string(word)
            if sorted_ch in dic:
                dic[sorted_ch].append(word)
            else:
                dic[sorted_ch] = [word]

    #         if len(word) > 21:
    #             print(word)
    # print(len(dic))
    # for key, val in dic.items():
    #     if len(key) >= 5 and len(val) >= 10:
    #         print(f'{key} : {val}')


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
    :return: none, update ans_lst
    """
    if len(s_4c) == 0:                                  # base case: when already choose all ch
        # if this is word in dictionary list and not in answer list, pass useless string
        if s_n in dic[sort_string(s_n)] and s_n not in ans_lst:   # if it's word in dic and not found before
            print(f'Found:  {s_n}')                     # print this word
            ans_lst.append(s_n)                         # save to answer list
            print('Searching...')                       # find 1 then searching next one

    else:                                               # recursion: when didn't choose all ch, need choose next one
        # Prune, if this prefix and the length of word are not in the dictionary, return this choose
        if not has_prefix(s_n, s_4c):
            return

        for i in range(len(s_4c)):                      # for loop to choose 1 ch(in s_4c) add to ans
            # Choose
            s_n += s_4c[i]                              # choose a new ch to string now
            # Explore
            ns_4c = s_4c[:i] + s_4c[i + 1:]             # update new string for choose, which send to next recursion
            find_anagrams_helper(ns_4c, s_n, ans_lst)   # recursion,
            # Un-choose
            s_n = s_n[:len(s_n) - 1]                    # string now pop last ch


def has_prefix(sub_s, s_4c):
    """
    :param sub_s: string, the prefix need to check in dictionary list or not
    :param s_4c:
    :return: bool
    """
    for word in dic[sort_string(sub_s+s_4c)]:
        if word.startswith(sub_s):                  # check word in dictionary has prefix or not
            return True


def sort_string(s):
    """
    :param s: string, ex: 'apple'
    :return: string, sorted by a,b,c,d,e... ex: 'aelpp'
    """
    sort_s = ''
    for ch in sorted(list(s)):
        sort_s += ch
    return sort_s


if __name__ == '__main__':
    main()
