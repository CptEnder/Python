"""
Created on Sat 14 Nov 11:27 2020
Finished on
@author: Cpt.Ender

https://www.codechef.com/BENDSP01/problems/BENDSP2
Chefina loves cakes! N suitors numbered 1…N have arrived from across the seven seas to woo her.

Each of the suitors wishes to impress Chefina, so suitor i has prepared a cake of height Hi.
To test the suitors, Chefina assigned them Q tasks. Each of the tasks is of one of the following types:

1 L R X: Increase the heights of all cakes in the range L to R inclusive by X, i.e.,
increase each of HL, HL+1, HL+2… HR by X.
2: Find the sum of heights of all cakes prepared by odd-numbered suitors.
3: Find the sum of heights of all cakes prepared by even-numbered suitors.
Can you help the suitors complete the tasks?

Input:
The first line contains an integer N, the number of cakes.
The next line contains N space-separated integers H1,H2,…,HN, denoting the heights of the cakes.
The third line contains an integer Q, the number of tasks.
The next Q lines describe the tasks assigned to the suitors by Chefina.
Output:
For each task of type 2 or 3, display the sum of heights of all cakes
prepared by odd or even-numbered suitors, respectively, on a new line.

Constraints:
1≤N≤105
1≤Q≤2⋅105
1≤L≤R≤N
1≤X,Hi≤108
Subtasks:
Subtask #1 (10% of the score): 1≤N,Q,X,Hi≤103.
Subtask #2 (10% of the score): 1≤N,Q≤103.
Subtask #3 (80% of the score): Original constraints.

Sample Input:
6
2 9 5 2 1 8
5
2
3
1 1 3 2
3
2
Sample Output:
8
19
21
12
Explanation:
Initially,

The sum of heights of cakes prepared by odd-numbered suitors is 2+5+1=8.
The sum of heights of cakes prepared by even-numbered suitors is 9+2+8=19.
After increasing the heights of cakes prepared by suitors 1, 2 and 3,

The sum of heights of cakes prepared by odd-numbered suitors becomes 4+7+1=12.
The sum of heights of cakes prepared by even-numbered suitors becomes 11+2+8=21.

Partially Correct Answer 20% - TLE (Time Limit Error) on Original Constrains
                                                                                       """
N = int(input())
H = [int(i) for i in input().split(' ')]
Q = int(input())
X = L = R = 0

for _ in range(Q):
    tasks = [int(n) for n in input().split(' ')]
    if tasks[0] == 1:
        [tasksID, L, R, X] = tasks
    else:
        tasksID = tasks[0]
    if tasksID == 3:
        sumEven = 0
        if not N % 2:
            end = N // 2
        else:
            end = N // 2 + 1
        for i in range(0, end):
            sumEven += H[(i * 2) + 1]
        print(sumEven)
    if tasksID == 2:
        sumOdd = 0
        if not N % 2:
            end = N // 2
        else:
            end = N // 2 + 1
        for i in range(0, end):
            sumOdd += H[i*2]
        print(sumOdd)
    if tasksID == 1:
        for i in range(L-1, R):
            H[i] += X
