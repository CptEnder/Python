"""
Created on Sun 09 May 13:17 2021
Finished on
@author: Cpt.

https://www.codechef.com/CDRL2021/problems/STRPER

Given a string, your task is to generate all different strings that can be created using its characters.

Input:
The only input line has a string of length n. Each character is between a–z.

Output:
First print an integer k: the number of strings. Then print k lines: the strings in alphabetical order.

Constraints
1≤n≤8

Sample Input:
abc

Sample Output:
6
abc
acb
bac
bca
cab
cba
                                  """

def factorial(N, nFact=1):
    if N == 0:
        return nFact
    return factorial(N - 1, nFact * N)


def lexicographical_permutations(string):
    # there are going to be n ! permutations where n = len(seq)
    fact = factorial(len(string))
    print(fact)
    for p in range(fact):
        lst.append(''.join(string))

        i = len(string) - 1

        # find i such that string[i:] is the largest sequence with
        # elements in descending lexicographic order
        while i > 0 and string[i - 1] > string[i]:
            i -= 1

        # reverse string[i:]
        string[i:] = reversed(string[i:])

        if i > 0:

            q = i
            # find q such that string[q] is the smallest element
            # in string[p:] such that string[q] > string[i - 1]
            while string[i - 1] > string[q]:
                q += 1

            # swap string[i - 1] and string[q]
            temp = string[i - 1]
            string[i - 1] = string[q]
            string[q] = temp

    lst.sort()


s = input()
s = list(s)
lst = []
lexicographical_permutations(s)
print(*lst)