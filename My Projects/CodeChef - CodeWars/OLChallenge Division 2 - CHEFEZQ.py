"""
Created on Sat 03 Oct 21:51 2020
Finished on
@author: Cpt.Ender

https://www.codechef.com/OCT20B/problems/CHEFEZQ
Chef published a blog post, and is now receiving many queries about it.
On day i, he receives Qi queries. But Chef can answer at most k queries in a single day.

Chef always answers the maximum number of questions that he can on any given day
(note however that this cannot be more than k).
The remaining questions (if any) will be carried over to the next day.

Fortunately, after n days, the queries have stopped.
Chef would like to know the first day during which he has some free time,
i.e. the first day when he answered less than k questions.

Input:
First line will contain T, the number of testcases. Then the testcases follow.
The first line of each testcase contains two space separated integers n and k.
The second line of each testcase contains n space separated integers, namely Q1,Q2,...Qn.
Output:
For each testcase, output in a single line the first day during which chef answers less than k questions.

Constraints
1≤T≤105
1≤ sum of n over all testcases ≤105
1≤k≤108
0≤Qi≤108
Subtasks
Subtask 1 - 20% points - Sum of Qi over all testcases and days ≤3.106
Subtask 2 - 80% points - Original constraints
Sample Input:
2
6 5
10 5 5 3 2 1
1 1
100
Sample Output:
6
101
                                  """
T = int(input())

for _ in range(T):
    _in = input().split(' ')
    N, K = int(_in[0]), int(_in[1])
    Q = [0 for _ in range(N)]
    _in = input().split(' ')
    for i, q in enumerate(_in):
        Q[i] = int(q)

    Day = 1
    carry = Q[Day - 1]
    while carry >= K:
        if Day < N:
            carry += Q[Day]
        carry -= K
        Day += 1
    print(Day)

""" PARTIALLY CORRECT ANSWER """
