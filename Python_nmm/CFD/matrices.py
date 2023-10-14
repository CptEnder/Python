"""
Created on Mon 09 Mar 11:26 2020
Finished on
@author: Cpt.Ender

Current features :  - Matrix addition/substraction
                    - Inverse matrix (Adjoint method)
                    - Detetrminant of a matrix
                    - Adjoint of a matrix
                    - Matrix multiplication
                    - Transpose of a matrix
                    - Inverse method (Gauss Elimination)-> faster method
                                                                        """


def I(n):
    """Creates an n × n square matrix with ones on the main diagonal and zeros elsewhere"""
    new_mat = []
    for i in range(n):
        new_mat.append([0 for j in range(n)])
        new_mat[i][i] = 1
    return new_mat


def zeros(n: int, m: int):
    """Creates an n x m matrix filled with zeros"""
    new_mat = []
    for i in range(n):
        new_mat.append([0 for j in range(m)])
    return new_mat


def ones(n: int, m: int):
    """Creates an n x m matrix filled with ones"""
    new_mat = []
    for i in range(n):
        new_mat.append([1 for j in range(m)])
    return new_mat

def det(A: list, d=1):
    """Returns the determinant of a matrix"""
    if len(A) == 2:
        d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
        return d

    new_mat = forwardElimination(A)
    for i in range(len(A)):
        d *= new_mat[i][i]
    return d


def sub(A: list, B: list):
    """Returns the substraction of two matrices of same size"""
    if type(A[0]) is not list:
        A = [A]
    if type(B[0]) is not list:
        B = [B]
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        print("Matrices must be of the same size")
        return
    new_mat = []
    for i in range(len(A)):
        new_mat.append([])
        for j in range(len(A[i])):
            new_mat[i].append(A[i][j] - B[i][j])
    if len(new_mat) == 1:
        new_mat = new_mat[0]
    return new_mat


def add(A: list, B: list):
    """Returns the addition of two matrices of same size"""
    if type(A[0]) is not list:
        A = [A]
    if type(B[0]) is not list:
        B = [B]
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        print("Matrices must be of the same size")
        return
    new_mat = []
    for i in range(len(A)):
        new_mat.append([])
        for j in range(len(A[i])):
            new_mat[i].append(A[i][j] + B[i][j])
    if len(new_mat) == 1:
        new_mat = new_mat[0]
    return new_mat


def mult(A: list, B: list):
    """Returns the dot product of two matrices"""
    if type(A[0]) is not list:
        A = [A]
    if type(B[0]) is not list:
        B = [B]
    if len(A[0]) != len(B):
        print("Matrices are not compatible")
        return
    new_mat = []
    for i in range(len(A)):
        new_mat.append([])
        for j in range(len(B[0])):
            sum = 0
            for k in range(len(B)):
                sum += A[i][k] * B[k][j]
            new_mat[i].append(sum)
    return new_mat


def swapRows(A: list, x, y):
    """Swaps two rows of a matrix"""
    new_mat = A[:]
    temp = A[x]
    new_mat[x] = new_mat[y]
    new_mat[y] = temp
    return new_mat


def multbynum(A: list, x):
    """Returns the multiplication of every element of the matrix with a number"""
    if type(A[0]) is not list:
        new_mat = [A[i] * x for i in range(len(A))]
    else:
        new_mat = A[:]
        for i in range(len(A)):
            new_mat[i] = multbynum(A[i], x)
    return new_mat


def transpose(A: list):
    """Returns the transpose of a matrix"""
    new_mat = []
    if type(A[0]) is not list:
        A = [A]
    for i in range(len(A[0])):
        new_mat.append([A[j][i] for j in range(len(A))])
    return new_mat


def adjoint(A: list):
    """Returns the adjoint of a matrix"""
    ad = []
    for i in range(len(A)):
        ad.append([0 for x in range(len(A))])
        for j in range(len(A)):
            sign = (-1) ** (j + i)
            if j == 0:
                sub_array = A[1:]
            elif j == len(A) - 1:
                sub_array = A[:j]
            else:
                sub_array = A[0:j] + [x for x in A[j + 1:]]
            for ii in range(len(sub_array)):
                sub_array[ii] = sub_array[ii][0:i] + sub_array[ii][i + 1:]
            ad[i][j] = sign * det(sub_array)
    return ad


def inverseMatrixAdj(A: list):
    """Returns the inverse of a matrix using the adjoint method"""
    d = det(A)
    adj = adjoint(A)
    if d != 0:
        inv = [[x / d for x in row] for row in adj]
        return inv
    else:
        print("Determinant = 0. There is no A^-1")


def inverseMatrix(A: list):
    """Returns the inverse of a matrix using the Gauss Elimination method"""
    if det(A) == 0:
        print("Determinant = 0. There is no A^-1")
        return
    inv = []
    for i in range(len(A)):
        inv.append(A[i][:] + I(len(A))[i][:])
    inv = gaussElimination(inv)
    for i in range(len(A)):
        inv[i] = inv[i][len(A):]
    return inv


#

# A = [[5,6,7],[8,9,10],[0,2,3]]
# A = [[2, 1, -1],[-3, -1,2],[-2, 1,2]]
# B = [[8], [-11], [-3]]
# B = [[2,4],[2,10]]
# A = [[1,2],[1,2]]
# B = [[2,3],[2,3]]
# C = add(A, B)
# C = linalgSolve(A, B)
# def frange(start, stop, step):
#     lst = []
#     start = float(start)
#     count = 0
#     while start + count*step <= float(stop):
#         lst.append(start + count*step)
#         count += 1
#     return lst
#
#
# n = 100
# dx = 1/n
# x = frange(0, 1, dx)
# e =  2.718281828459045
# f = [-(3*i + i**2)*e**i for i in x]
#
# a = []
# for i in range(n+1):
#     a.append([0*k for k in range(n+1)])
#     if 0 < i < n:
#         a[i][i-1] = 1
#         a[i][i] = -2
#         a[i][i+1] = 1
# a[0][0] = a[n][n] = 1
# f[0] = f[n] = 0
#
# c = linalgSolve(a,f)
# d = det(a)
