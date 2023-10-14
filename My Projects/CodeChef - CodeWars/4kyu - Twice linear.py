"""
Created on Fri 17 Feb 17:06 2023
Finished on Thu 23 Feb 18:00 2023
@author: Cpt.Ender

https://www.codewars.com/kata/5672682212c8ecf83e000050

Consider a sequence u where u is defined as follows:

The number u(0) = 1 is the first one in u.
For each x in u, then y = 2 * x + 1 and z = 3 * x + 1 must be in u too.
There are no other numbers in u.
Ex: u = [1, 3, 4, 7, 9, 10, 13, 15, 19, 21, 22, 27, ...]

1 gives 3 and 4, then 3 gives 7 and 10, 4 gives 9 and 13,
then 7 gives 15 and 22 and so on...

Task:
Given parameter n the function dbl_linear (or dblLinear...)
returns the element u(n) of the ordered (with <) sequence u (so, there are no duplicates).

Example:
dbl_linear(10) should return 22

Note:
Focus attention on efficiency
                                  """
import time


# def dbl_linear(n):
#     u = dict.fromkeys([1])
#     i = 0
#     x = 1
#     while len(u) < n + 1 or sorted(list(u.keys()))[n] > x * 2+1:
#         x = sorted(list(u.keys()))[i]
#         y = 2 * x + 1
#         z = 3 * x + 1
#         u[y] = None
#         u[z] = None
#         i += 1
#     return sorted(list(u.keys())), sorted(list(u.keys()))[n]


# def dbl_linear(n):
#     u = [1, 3, 4]
#     i = 1
#     x = u[i]
#     while len(u) < n + 1 or u[n] > 2 * x + 1:
#         y = 2 * x + 1
#         ii = -1
#         while y < u[ii]:
#             ii -= 1
#         if y > u[ii]:
#             u = u[:len(u) + ii + 1] + [y] + u[len(u) + ii + 1:]
#         z = 3 * x + 1
#         u.append(z)
#         i += 1
#         x = u[i]
#     return u[n]

def dbl_linear(n):
    u = [1, 3, 4]
    i = j = 1
    while len(u) <= n:
        if 2 * u[i] + 1 <= 3 * u[j] + 1:
            if not 2 * u[i] - 3 * u[j]:
                j += 1
            u.append(2 * u[i] + 1)
            i += 1
        if 3 * u[j] + 1 < 2 * u[i] + 1:
            u.append(3 * u[j] + 1)
            j += 1
    return u[n]


start = time.time()
b = dbl_linear(15000)
# for v in range(300, 1300):
#     b = dbl_linear(v)
#     # print(b)
print(time.time() - start)
