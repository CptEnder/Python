"""
Created on Thu 13 May 12:42 2021
Finished on
@author: Cpt.Ender

https://www.codechef.com/MAY21C/problems/ISS

Zanka finds fun in everyday simple things.
One fine day he got interested in a very trivial sequence.
Given a natural number k, he considers the sequence Ai=k+i2 so that the terms are

k+1,k+4,k+9,k+16,…
Now to make things more interesting, he considers the gcd of consecutive terms in the sequence,
then takes the sum of the first 2k values. More formally, he wants to compute

∑i=1,2k gcd(Ai,Ai+1)
Denote this sum by S. Zanka wants you to print the number S for each k.

Input
The first line contains an integer T, the number of test cases. Descriptions of test cases follow.
The only line of each test case contains a single integer k.
Output
For each test case, output a single line containing the sum S for the given k.

Constraints
1≤T≤106
1≤k≤106

Subtasks
Subtask #1 (20 points): t≤103,k≤103
Subtask #2 (80 points): Original Constraints

Sample Input
1
1

Sample output
6

Explanation
The first 2k+1 terms of the sequence A are 2,5,10.

So the answer is gcd(2,5)+gcd(5,10)=1+5=6

TLE
                                  """


# def gcd(a, b):
#     while b:
#         a, b = b, a % b
#     return a

# def gcd(a, b):
#     # Base cases
#     # gcd(n, n) = n
#     if a == b:
#         return a
#
#     # Identity 1: gcd(0, n) = gcd(n, 0) = n
#     if a == 0:
#         return b
#     if b == 0:
#         return a
#
#     if a & 1:  # a is odd
#         if not b & 1:  # b is even
#             return gcd(a, b // 2)
#
#         # Identities 3 and 4
#         if a > b:
#             return gcd((a - b) // 2, b)
#         else:
#             return gcd((b - a) // 2, a)
#     else:  # a is even
#         if b & 1:  # b is odd
#             return gcd(a // 2, b)  # Identity 3
#         else:  # both even
#             return 2 * gcd(a // 2, b // 2)  # Identity 2

def countTrailingZeros(x):
    count = 0
    while (x & 1) == 0:
        x = x >> 1
        count += 1

    return count


def gcd(u, v):
    if u == 0:
        return v
    if v == 0:
        return u
    shift = countTrailingZeros(u | v)
    u >>= countTrailingZeros(u)
    while v != 0:
        v >>= countTrailingZeros(v)
        if u > v:
            t = v
            v = u
            u = t
        v = v - u

    return u << shift


# T = int(input())
T = 100
k = 0
for _ in range(T):
    k += 1
    S = 0
    print('----------------------')
    for i in range(1, 2 * k + 1):
        print(gcd(k + i ** 2, k + (i + 1) ** 2))
        S += gcd(k + i ** 2, k + (i + 1) ** 2)

    print(S)
