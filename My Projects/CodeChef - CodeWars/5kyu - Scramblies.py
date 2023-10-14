"""
Created on Mon 06 Feb 22:33 2023
Finished on
@author: Cpt.Ender

https://www.codewars.com/kata/55c04b4cc56a697bb0000048

Complete the function scramble(str1, str2) that returns true
if a portion of str1 characters can be rearranged to match str2, otherwise returns false.

Notes:

Only lower case letters will be used (a-z). No punctuation or digits will be included.
Performance needs to be considered.
Examples
scramble('rkqodlw', 'world') ==> True
scramble('cedewaraaossoqqyt', 'codewars') ==> True
scramble('katas', 'steak') ==> False
                                                                    """


def scramble(str1, str2):
    arr = dict.fromkeys(list(str2), 0)
    for c in str2:
        arr[c] += 1

    for c in str1:
        if c in arr.keys():
            arr[c] -= 1

    for v in arr.values():
        if v > 0:
            return False
    return True


sc = scramble('cedewaraaossoqqyt', 'codewars')
