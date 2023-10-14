"""
Created on Sun 09 May 12:33 2021
Finished on Sun 09 May 12:35 2021
@author: Cpt.Ender

https://www.codechef.com/CDRL2021/problems/TABLE

You are teaching a kid to remember the multiplication table and
meanwhile get urgent work and you have to leave in the next five minutes.

So to avoid interruption in kid's practice you want to code a
program that takes an integer N as input and outputs its multiplication table.

Input:
The first input line has an integer N.

Output:
Output the multiplication table of N.

Constraints
1≤N≤1000

Sample Input:
7

Sample Output:
7 -> 14 -> 21 -> 28 -> 35 -> 42 -> 49 -> 56 -> 63 -> 70

(There is a single space between '7' and '->' and a single space between '->' and '14' and so on)

Completed
                                                                                                """
N = int(input())

string = str(N)
for i in range(2, 11):
    string += ' -> ' + str(N * i)

print(string)
