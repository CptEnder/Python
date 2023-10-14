"""
Created on Sat 22 May 19:29 2021
Finished on
@author: Cpt.Ender

https://www.codechef.com/CDIG2021/problems/AKA1

A student x participated in a coding contest. Rules of contest are as follows:

Their are total n number of questions in the contest.
Each question should be solved in k hours after that question will be disable.
You are given a series of integer array time and an integer k.
Where ith index denote time when ith question was asked.
When a question is asked participant has k duration of time to solve the question
(that is question can be solved between the time interval [time[i],time[i]+k−1] inclusive).

Return the maximum amount of time that the x can spend in solving all questions.

Input:
First line will contain n and k number of questions and time duration.
Second line will contain n integers at which represent the time when question will be ask.

Output:
Output in a single line answer.

Constraints
1≤n≤104
0≤time[i],k≤107

Sample Input:
2 3
1 2

Sample Output:
4

EXPLANATION:
At time point 1, x starts solving the question. This question will last 3 hours until the end of time point 3.

However, at the beginning of time point 2, x get new question but he is solving the previous question.

Since the time status won't add up together as at a time he can solve only one question,
though he can solve the second question till the end of time point 4.

So your final output is 4.

WA
                                  """
_in = input().split(' ')

[n, k] = [int(_) for _ in _in]

_in = input().split(' ')
arr = [int(_) for _ in _in]

maxDur = k

for i in range(len(arr) - 1):
    if arr[i + 1] <= arr[i] + k - 1:
        maxDur += arr[i + 1] - arr[i]
    else:
        maxDur += k

print(maxDur)
