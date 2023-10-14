"""
Created on Sat 22 May 20:07 2021
Finished on
@author: Cpt.Ender

https://www.codechef.com/CDIG2021/problems/AKA3

A farmer is going to the city for selling the mangoes.
He has N bags and each bag has some kgs of mangoes.
In the midway to the city he start feeling tired so he decide to distribute the weight of mango's bag.

He has an integer array weight where the ith bag has weight[i] kg of weight and given an integer K.

He can perform the following operation at most K times:

Take any bag of mangoes and divide it into two new bags with positive number of mangoes.
Example: if a bag 4kg mangoes can become two new bags of 1 kg and 3 kg, or two new bags of 2kg and 2kg mangoes.

For this farmer has to give the penalty.
Penalty is the bag with maximum kgs of mangoes.
He want to minimize his penalty after the operations.

Return the minimum possible penalty after performing the operations.

Input:
First line will contain N, K.
Second line contains N integers representing weights of N bags .

Output:
Output in a single line answer.

Constraints
1≤N≤1000
2≤weight[i],K≤109

Sample Input:
1 2
18

Sample Output:
6

EXPLANATION:
Divide the bag with 18 kgs mangoes into two bags of 12 kgs and 6 kgs.
Divide the bag with 12 kgs mangoes into two bags of 6 kgs and 6 kgs.
So farmer's penalty is 6 kgs of mangoes.
                                  """
_in = input().split(' ')
[N, K] = [int(_) for _ in _in]

_in = input().split(' ')
arr = [int(_) for _ in _in]

