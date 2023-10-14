"""
Created on Sun 09 May 12:38 2021
Finished on Sun 09 May 12:45 2021
@author: Cpt.Ender

https://www.codechef.com/CDRL2021/problems/DIVSTEST

You are given a number N. If the number is divisible by 5, 15, and 75
print 3 else if it is divisible by any two print 2 else
if it is divisible by any one print 1 and if it's not divisible by anyone print 0.

Input:
The first line contains the number of test cases T followed by N for each test case

Output:
Print 1, 2, or 3 in the new line.

Constraints
1≤N≤109

Sample Input:
2
15
95

Sample Output:
2
1

Completed
                                                    """
T = int(input())

for i in range(T):
    N = int(input())

    if N % 75 == 0 and N % 15 == 0 and N % 5 == 0:
        print(3)
    elif (N % 75 == 0 and N % 15 == 0) or (N % 15 == 0 and N % 5 == 0) or (N % 75 == 0 and N % 5 == 0):
        print(2)
    elif N % 75 == 0 or N % 15 == 0 or N % 5 == 0:
        print(1)
    else:
        print(0)