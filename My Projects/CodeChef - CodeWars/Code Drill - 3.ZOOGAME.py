"""
Created on Sun 09 May 12:49 2021
Finished on
@author: Cpt.Ender

https://www.codechef.com/CDRL2021/problems/ZOOGAME

You are playing a game with friends. This game requires entering a word
that consists of x and y that denote the number of Zs and Os respectively.
The input word is considered similar to the word zoo if 2∗x=y.

For winning the word needs to be similar to the zoo.

For your reference, consider words such as 'zzzooooo' and 'zzzzoooooooo'
are similar to the word zoo but not the words such as 'zzoooozo' and 'zzzzoooooooo'.

Input format

You are required to enter a word that consists of and that denotes
the number of Zs and Os respectively. The input word is considered similar to the word zoo if.

Determine if the entered word is similar to the word zoo.

For example, words such as 'zzoooo' and 'zzzoooooo' are similar
to the word zoo but not the words such as 'zzooo' and 'zzzooooo'.

Input:
First line will contain a single string S consisting of characters 'z' and 'o' only.

Output:
Print "Yes" if the input word can be considered as the string zoo otherwise, print "No".

Constraints
3≤ Length of String ≤20

Sample Input:
zzzoooooo

Sample Output:
Yes

Explanation:
zzzoooooo is similar to zoo

Wrong
                                  """
s = input()

zCount = s.count('z')

if zCount*2 != s.count('o'):
    print('No')
else:
    if s[:zCount] != 'z'*zCount:
        print('No')
    else:
        print('Yes')
