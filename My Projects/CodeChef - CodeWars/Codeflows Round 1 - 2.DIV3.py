"""
Created on Sat 14 Nov 12:21 2020
Finished on Sat 14 Nov 12:50 2020
@author: Cpt.Ender

https://www.codechef.com/BENDSP01/problems/DIV3
Let's consider some multiset A consisting of 0s, 1s, and 2s. Define S(A) to be the sum of the elements in A.

It is guaranteed that S(A) is divisible by 3.
You need to partition A into some number of nonempty multisets A1,A2,…,Ak such that:

A1∪A2∪…∪Ak=A
for all 1≤i≤k, S(Ai) is divisible by 3
You are given s0, s1, and s2, where si is equal to the number of occurrences of i in A.
Find the maximum possible value of k.

Input:
The first line contains one integer number t - the number of test cases. The next t lines describe test cases.

The only line of each test case contains three integers
s0, s1, and s2 - the number of 0s, 1s, and 2s in A, respectively.

Output:
For each test case print the maximum number of nonempty
multisets with sum divisible by 3 into which the multiset A can be partitioned.

Constraints
1 ≤ t ≤ 10^5
0 ≤ s0,s1,s2 ≤ 10^9

Subtasks
Subtask #1 (30 points): t ≤ 1000, s0,s1,s2 < 10
Subtask #2 (70 points): original constraints

Sample Input:
4
239 0 0
2 4 1
0 0 3
7 3 3
Sample Output:
239
4
1
10

Explanation:
In the first test case, we can divide our set into 239 sets with one zero in each
set because all numbers are divisible by 3. It is obvious that the number of sets can't be bigger.

In the second test case we can divide our set A={0,0,1,1,1,1,2}
into four sets {0},{0},{1,1,1},{1,2}. It can be proven that 4 is the maximum possible answer.

Correct Answer 100%
                                                                                              """

t = int(input())

for _ in range(t):
    [s0, s1, s2] = [int(n) for n in input().split(' ')]
    k = s0

    if s1 == s2:
        k += s1
    if s1 >= s2 + 3:
        k += s2 + (s1 - s2) // 3
    if s2 >= s1 + 3:
        k += (s2 - s1) // 3
        k += s1

    print(k)
