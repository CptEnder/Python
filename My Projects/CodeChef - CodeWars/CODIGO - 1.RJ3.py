"""
Created on Sat 22 May 19:11 2021
Finished on Sat 22 May 19:15 2021
@author: Cpt.Ender

https://www.codechef.com/CDIG2021/problems/RJ3

Ravi's summer vacation has started and he is feeling sleepy all the day.
As he is fond of solving questions, he decided to utilize these vacations.
He makes a plan of solving questions in following manner:-

On first day he solves 1 question , then on second day 2 questions,
then on third day 4 questions and so on that means with each passing day ,
number of questions will get doubled. But on some days,
due to his laziness he just sleeps all the day and doesn't practice a single question.

Now you are given an integer N denoting the total number
of questions he solved in the vacation . Determine the number of days he was active.
An active day means solving all the questions of that particular day.

Input:
First line will contain a single integer T determining number of test cases.

The only line in each test cases will consists of a single integer N determining number of questions done by Ravi.

Output:
Print number of days Ravi was active for each test case in a new line.

Constraints
1<=T<=100000

1<=N<=10^18

Sample Input:
2
10
20

Sample Output:
2
2

EXPLANATION:
For 1st test case, he was active on DAY 2 (2 questions) and DAY 4 (8 questions), so answer is 2.

COMPLETED
                                  """

T = int(input())

for _ in range(T):
    N = int(input())

    print(bin(N).count('1'))