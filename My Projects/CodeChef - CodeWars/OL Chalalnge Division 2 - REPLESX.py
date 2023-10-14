"""
Created on Mon 05 Oct 20:04 2020
Finished on
@author: Cpt.Ender

https://www.codechef.com/OCT20B/problems/REPLESX
You are given an array of N integers A1,A2,…,AN and three more integers X,p, and k.

An operation on the array is defined to be:
replace the k-th smallest integer in the array with any integer you want.

Output the minimum number of operations you must perform on the array
(possibly 0 operations) to make the p-th smallest element of the array equal to X.
If it is impossible to do so output −1.

Note: the k-th smallest number in an array is the k-th number
from the left when the array is sorted in non-decreasing order.

Input
The first line of the input contains a single integer T denoting the number of test cases
The first line of each test case contains four integers N,X,p,k respectively.
The second line of each test case contains N space-separated integers A1,A2,…,AN.

Output
For each test case, print a single line containing one integer ―
the minimum number of operations you must perform to make X the p-th smallest element
or −1 if its impossible to do so.

Constraints
1≤T≤100
1≤p,k≤N
0≤X≤109
The sum of N over all test cases does not exceed 4∗105
0≤Ai≤109 for each valid i
Subtasks
Subtask #1 (10 points): N≤5
Subtask #2 (40 points): The sum of N over all test cases does not exceed 3∗103
Subtask #3 (50 points): Original constraints

Example Input
2
5 4 3 4
4 9 7 0 8
2 25 1 2
100 20
Example Output
1
-1
                                  """
T = int(input())

for _ in range(T):
    infected = []
    _in = input().split(' ')
    [N, X, p, k] = [int(_in[i]) for i in range(len(_in))]
    _in = input().split(' ')
    arr = []
    for i in range(N):
        arr.append(int(_in[i]))