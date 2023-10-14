"""
Created on Mon 09 Mar 20:09 2020
Finished on
@author: Cpt.Ender

Current features :
    - Solving linear equations using Gauss Elimination
    - Solving diagonal linear equations using forward elimination
                                                                        """
from matrices import transpose, add, multbynum


def forwardElimination(A: list):
    """Returns the upper triangular matrix of A"""
    new_mat = A[:]
    for j in range(len(A[0]) - 1):
        for i in range(j + 1, len(A)):
            var = -new_mat[i][j] / new_mat[j][j]
            temp = new_mat[i]
            new_mat[i] = multbynum(new_mat[j], var)
            new_mat[i] = add(new_mat[i], temp)
    return new_mat


def gaussElimination(A: list):
    # Forward Elimination
    new_mat = forwardElimination(A)
    # Back substitution
    for i in range(len(A)):
        var = 1 / new_mat[i][i]
        new_mat[i] = multbynum(new_mat[i], var)
    for i in range(1, len(A)-1):
        for j in range(i, len(A)):
            var = -new_mat[-1-j][-1-i]
            pivot_row = multbynum(new_mat[-i], var)
            new_mat[-1-j] = add(new_mat[-1-j], pivot_row)
    return new_mat


def gesgae(A: list, B: list):
    """ Returns the solution for linear equations
        using the Gauss Elimination method.
        The A matrix can be anything.
        gesgae = general solution gauss elimination"""
    if len(A) != len(B) or type(B[0]) is not list:
        B = transpose(B)
    C = []
    for i in range(len(A)):
        C.append(A[i] + B[i])
    X = transpose(gaussElimination(C))[-1]
    return X


def dias(A: list, B: list, m: int):
    """ Returns the solution for linear equations where A
        is an n x n square diagonal matrix, m is the number of A's
        diagonals that are not 0, B is an n x 1 matrix,
        C is the joined matrix of A and B(n x n+1),
        and X is the solution matrix (1 x n)"""
    if len(A) != len(B) or type(B[0]) is not list:
        B = transpose(B)
    C = []
    for i in range(len(A)):
        C.append(A[i] + B[i])
    U = forwardElimination(C)
    X = [0 for i in range(len(A))]
    start = int((m-1)/2)
    for index in range(start, len(A) - start):
        i = len(A) - 1 - index
        s = U[i][-1]
        for ii in range(1, int(m - start)):
            s -= U[i][i+ii]*X[i+ii]
        X[i] = s / U[i][i]
    for i in range(start):
        X[i] = U[i][-1]/U[i][i]
        X[-1-i] = U[-1-i][-1]/U[-1-i][-2-i]

    return X
