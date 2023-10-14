"""
Created on Sat 14 Nov 13:24 2020
Finished on
@author: Cpt.Ender

The beauty of an array A1,A2,…,AN is defined by the following formula:
∏i=1:N(∏j=i:N(min(Ai,Ai+1,…,Aj))).
You are given two integers X and P where P is prime. You have to find an array A such that

1≤N≤2000
0≤Ai≤100 for each i from 1 to N
The beauty of A is equivalent to X modulo P.
If there is no solution under such constraints then just output "-1" (without quotes).

Input
The first line of the input contains a single integer T denoting the number of test cases.
The descriptions of T test cases follow.
The first and only line of each test case contains two space-separated integers X and P.
Output
For each test case, print the answer in the following way:

If a solution exists then on the first line print N, the length of the array A.
On the next line, print N space-separated integers, the elements of A.
If there are multiple solutions, you can print any.
If there is no solution then just output "-1" (without quotes).

Constraints
1 ≤ T ≤ 1000
0 ≤ X < P≤ 106
P is prime.

Example Input
3
1 7
5 19
0 13
Example Output
3
2 2 2
6
2 4 11 5 7 4
2
1 13
Explanation:
Sample case 1: The beauty is equal to 26=64, which has remainder 1 when divided by 7.

Sample case 2: The beauty is equal to 26⋅49⋅54⋅7⋅11=807,403,520,000, which has remainder 5 when divided by 19.

Sample case 3: The beauty is equal to 12⋅13=13, which has remainder 0 when divided by 13.
                                                                                                            """


def beauty(array: list):
    product = 1
    for i in range(len(array)):
        for j in range(1, len(array)):
            product *= min(array[i:j])
    return product


beauty([2, 2, 2])
