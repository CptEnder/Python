"""
Created on Sat 03 Oct 22:34 2020
Finished on
@author: Cpt.Ender

https://www.codechef.com/OCT20B/problems/POSAND
A permutation p1,p2...pN of {1,2,...,N} is beautiful if pi&pi+1 is greater than 0 for every 1≤i<N.
You are given an integer N, and your task is to construct a beautiful permutation of length N
or determine that it's impossible.

Note that a&b denotes the bitwise AND of a and b.

Input:
First line will contain T, number of testcases.
Then the testcases follow. Each testcase contains a single line of input, an integer N.

Output:
For each test case output −1 if there is no suitable permutation of length N,
otherwise output N integers in a single line which form a beautiful permutation.
If there are multiple answers output any of them.

Constraints
1≤N≤105
The sum of N over all test cases does not exceed 106
Subtasks
50 points : 1≤N,T≤9
50 points : Original constraints

Sample Input:
3
4
3
5
Sample Output:
-1
1 3 2
2 3 1 5 4
                                  """


def check(_lst: list):
    new_lst = []
    for _i in range(len(_lst) - 1):
        new_lst.append(_lst[_i] & _lst[_i + 1])
    return new_lst.count(0)


def posAnd(num: int, end: int):
    _powerOf2 = len(bin(num)) - 3
    if _powerOf2 == 0:
        permutation.append(1)
        return
    for n in range(2 ** _powerOf2, end + 1):
        permutation.append(n)
    posAnd(2 ** (_powerOf2 - 1), 2 ** _powerOf2 - 1)


T = int(input())

for _ in range(T):
    N = int(input())
    # N = _
    if not N % 500:
        print(N)

    permutation = []
    if bin(N).count('1') == 1:
        print(-1)
        continue
    else:
        if N % 2:
            powerOf2 = len(bin(N)) - 3
            posAnd(2 ** (powerOf2 - 1), 2 ** powerOf2 - 1)
            for i in range(N, 2 ** powerOf2 - 1, -1):
                permutation.append(i)
        else:
            powerOf2 = len(bin(N - 1)) - 3
            posAnd(2 ** (powerOf2 - 1), 2 ** powerOf2 - 1)
            for i in range(N - 1, 2 ** powerOf2 - 1, -1):
                permutation.append(i)
            permutation.append(N)
        # print(*permutation)
    # Not needed
    checker = check(permutation)
    if checker > 0:
        print(N)

""" PARTIALLY CORRECT ANSWER """
