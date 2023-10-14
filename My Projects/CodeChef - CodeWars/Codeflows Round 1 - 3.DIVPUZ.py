"""
Created on Sat 14 Nov 17:17 2020
Finished on
@author: Cpt.Ender

https://www.codechef.com/BENDSP01/problems/DIVPUZ
You are given an array of positive integers a1,a2,…,an.

You should find another array of positive integers b1,b2,…,bn that satisfies the following conditions:

For all 1≤i≤n, bi≤10^18.
For all 1≤i≤n, ai divides bi.
For all 1≤i≤n, bi divides bi−1⋅bi+1 (we consider b0=bn and bn+1=b1).
Input:
The first line contains an integer t - the number of test cases. The next 2t lines describe test cases.

The first line of each test case contains a positive integer n.

The second line of each test case contains n positive integers a1,a2,…,an - the given array.

Output:
For each test case print n positive integers b1,b2,…,bn that satisfy all the conditions above.

The constraints guarantee that an answer always exists. If there exist multiple answers you can print any.

Constraints
1 ≤ t ≤ 10^5
3 ≤ n ≤ 100000
1 ≤ ai ≤ 10^9
the sum of n for all test cases does not exceed 300000
Subtasks
Subtask #1 (30 points): n is even, ai = 1 for all even i
Subtask #2 (70 points): Original Constraints

Sample Input:
4
3
2 3 9
5
1 1 1 1 1
3
6 10 15
4
2 3 4 5
Sample Output:
54 54 54
2 4 2 4 2
6 10 15
30 6 4 10
Explanation:
Let's consider the fourth test case. For all i, ai divides bi, as

2 divides 30
3 divides 6
4 divides 4
5 divides 10
For all i, bi divides bi−1⋅bi+1, as

30 divides 10⋅6=60
6 divides 30⋅4=120
4 divides 6⋅10=60
10 divides 4⋅30=120
                                                                      """
t = int(input())

for _ in range(t):
    n = int(input())
    A = [int(a) for a in input().split(' ')]
    B = A[:]
    B1 = B[:]
    for i in range(len(B)):
        index1 = i - 1
        if i == len(B) - 1:
            index2 = 0
        else:
            index2 = i + 1
        if B[i] < B[index1]*B[index2]:
            if B[index2] * B[index1] / B[i] % 1:
                B1[i] *= B[index1] * B[index2]
        else:
            tempList = [B[index1], B[index2]]
            tempIndexList = [index1, index2]
            indexMinInList = tempList.index(min(tempList))
            indexMin = tempIndexList[indexMinInList]
            indexMax = tempIndexList[indexMinInList^1]
            B1[indexMin] = B[indexMax]*B[i]

    print(*B1)
