"""
Created on Sun 18 Apr 01:15 2021
Finished on Sun 18 Apr 01:40 2021
@author: Cpt.Ender

https://www.codechef.com/IARCSJUD/problems/LONGPALI

As we all know, a palindrome is a word that equals its reverse.
Here are some examples of palindromes: malayalam, gag, appa, amma.

We consider any sequence consisting of the letters of the English alphabet to be a word.
So axxb,abbba and bbbccddx are words for our purpose. And aaabbaaa, abbba and bbb are examples of palindromes.

By a subword of a word, we mean a contiguous subsequence of the word.
For example the subwords of the word abbba are a, b, ab, bb, ba, abb, bbb, bba, abbb, bbba and abbba.

In this task you will given a word and you must find the longest
subword of this word that is also a palindrome.

For example if the given word is abbba then the answer is abbba.
If the given word is abcbcabbacba then the answer is bcabbacb.

Input:
The first line of the input contains a single integer N indicating the length of the word.
The following line contains a single word of length N, made up of the letters a,b,…, z.

Output:
The first line of the output must contain a single integer indicating the
length of the longest subword of the given word that is a palindrome.
The second line must contain a subword that is a palindrome and which of maximum length.
If there is more than one subword palindrome of maximum length, it suffices to print out any one.

Constraints:
1≤N≤5000.
You may assume that in 30% of the inputs 1≤N≤300.
Sample Input 1:
5
abbba

Sample Output 1:
5
abbba

Sample Input 2:
12
abcbcabbacba

Sample Output 2:
8
bcabbacb

Completed
                                  """
N = int(input())

Word = input()


def checkIfPalindrome(word: str, n: int):
    if n % 2 == 0:
        if word[:n // 2] == word[-n // 2:][::-1]:
            return True
        else:
            return False
    else:
        if word[:n // 2] == word[-n // 2 + 1:][::-1]:
            return True
        else:
            return False


currentN = N
while currentN >= 1:
    for i in range(N - currentN + 1):
        if checkIfPalindrome(Word[i:currentN + i], currentN):
            print(currentN)
            print(Word[i:currentN + i])
            N = 0
            break
    currentN -= 1
