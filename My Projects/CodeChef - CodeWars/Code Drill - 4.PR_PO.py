"""
Created on Sun 09 May 12:58 2021
Finished on
@author: Cpt.Ender

https://www.codechef.com/CDRL2021/problems/PR_PO

The principal has asked you to rotate the array in such a manner
that the student at position number K will be at the last position
(After rotation ) in 0 based indexing, i.e., if K=2 then the last two students will be the first two.

Input:
The first line will consist of one integer T denoting the number of test cases. For each test case:
The first line consists of two integers N and K, N being the number
of elements in the array and K denotes the number of steps of rotation.
The next line consists of N space-separated integers, denoting the elements of the array A.

Output:
Print all the elements of the rotated array followed by a space.

Constraints
1≤T≤1000
0≤K≤100
0≤N≤100
0≤Ai≤105

Sample Input:
1
5 2
1 2 3 4 5

Sample Output:
4 5 1 2 3

EXPLANATION:
Here T is 1, which means one test case.
N=5 denoting the number of elements in the array and K=2, denoting the number of steps of rotations.
The initial array is: 1 2 3 4 5
In the first rotation, 5 will come in the first position and
all other elements will move to one position ahead of their current position.
Now, the resultant array will be 5 1 2 3 4 In the second rotation,
4 will come in the first position and all other elements will move to one position
ahead of their current position. Now, the resultant array will be 4 5 1 2 3
                                                                                    """

T = int(input())

for i in range(T):
    _in = input().split(' ')
    [N, K] = [int(_in[k]) for k in range(2)]
    _in = input().split(' ')
    A = [int(_in[k]) for k in range(N)]

    B = A[K+1:]
    B.extend(A[:K+1])
    print(*B)
