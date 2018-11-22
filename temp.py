# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from mpi4py import MPI

def fillMat(A, B, n):
    for i in range(n):
        for j in range(n):
            A[i][j]= i+j;
            if i == j:
                B[i][j] = 2
            else:
                B[i][j] = 0
    return A, B

def printMatrix(matrix, n):
    for i in range(n):
        for j in range(n):
            print(matrix[i][j], end=' ')
        print()
        
def add(A, B):
    n = len(A)
    C = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            C[i][j] = A[i][j] + B[i][j]
    return C

def subtract(A, B):
    n = len(A)
    C = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            C[i][j] = A[i][j] - B[i][j]
    return C

def multiply(A, B):
    n = len(A)
    C = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            for k in range(0, n):
                C[i][j] = C[i][j] + A[i][k] * B[k][j]         
    return C

def strass(A, B, n, total, communicator):
    #determines the number of recursion, //2 for 1st lvl, //4 for 2nd, //8 for 3rd
    if n == total//2:
        return multiply(A, B)
    
    #else.... proceed
    newSize = n//2
    a11 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
    a12 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
    a21 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
    a22 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]

    b11 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
    b12 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
    b21 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
    b22 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
    
    for i in range(0, newSize):
        for j in range(0, newSize):
            a11[i][j] = A[i][j]            # top left
            a12[i][j] = A[i][j + newSize]    # top right
            a21[i][j] = A[i + newSize][j]    # bottom left
            a22[i][j] = A[i + newSize][j + newSize] # bottom right

            b11[i][j] = B[i][j]            # top left
            b12[i][j] = B[i][j + newSize]    # top right
            b21[i][j] = B[i + newSize][j]    # bottom left
            b22[i][j] = B[i + newSize][j + newSize] # bottom right
    
    if n == total:
        id = communicator.Get_rank()
        size = communicator.Get_size()
        for i in range(0,size):
            if i == 0:
                if id == i:
                    p1 = strass(add(a11, a22), add(b11, b22), newSize, total,communicator)
            elif i == 1:
                if id == i:
                    p2 = strass(add(a21, a22), b11, newSize, total,communicator)
                    communicator.send(p2, dest=0, tag = 1)
            elif i == 2:
                if id == i:
                    p3 = strass(a11, subtract(b12, b22), newSize, total,communicator)
                    communicator.send(p3, dest=0, tag = 1)
            elif i == 3:
                if id == i:
                    p4 = strass(a22, subtract(b21, b11), newSize, total,communicator)
                    communicator.send(p4, dest=0, tag = 1)
            elif i == 4:
                if id == i:
                    p5 = strass(add(a11, a12),b22, newSize, total,communicator)
                    communicator.send(p5, dest=0, tag = 1)
            elif i == 5:
                if id == i:
                    p6 = strass(subtract(a21, a11), add(b11, b12), newSize, total,communicator)
                    communicator.send(p6, dest=0, tag = 1)
            elif i == 6:
                if id == i:
                    p7 = strass(subtract(a12, a22), add(b21, b22), newSize, total,communicator)
                    communicator.send(p7, dest=0, tag = 1)
        if id == 0:
            p2 = communicator.recv(source = 1, tag = 11)
            p3 = communicator.recv(source = 2, tag = 11)
            p4 = communicator.recv(source = 3, tag = 11)
            p5 = communicator.recv(source = 4, tag = 11)
            p6 = communicator.recv(source = 5, tag = 11)
            p7 = communicator.recv(source = 6, tag = 11)
            
            c11 = add(subtract(add(p1, p4),p5), p7)
            c12 = add(p3, p5)
            c21 = add(p2, p4)
            c22 = add(add(subtract(p1, p2), p3), p6)
            
            result1 = [[0 for j in range(0, n)] for i in range(0, n)]
    
            for i in range(0, newSize):
                for j in range(0, newSize):
                    result1[i][j] = a11[i][j] = c11[i][j]            # top left
                    result1[i][j + newSize] = c12[i][j]     # top right
                    result1[i + newSize][j] = c21[i][j]    # bottom left
                    result1[i + newSize][j + newSize] = c22[i][j]  # bottom right
        
        result = communicator.bcast(result1, root = 0)
        print('Matrix C = AB')
        printMatrix(result, n)
        return result;
        
        
        
    p1 = strass(add(a11, a22), add(b11, b22), newSize, total,communicator)
    p2 = strass(add(a21, a22), b11, newSize, total,communicator)
    p3 = strass(a11, subtract(b12, b22), newSize, total,communicator)
    p4 = strass(a22, subtract(b21, b11), newSize, total,communicator)
    p5 = strass(add(a11, a12),b22, newSize, total,communicator)
    p6 = strass(subtract(a21, a11), add(b11, b12), newSize, total,communicator)
    p7 = strass(subtract(a12, a22), add(b21, b22), newSize, total,communicator)
    
    c11 = add(subtract(add(p1, p4),p5), p7)
    c12 = add(p3, p5)
    c21 = add(p2, p4)
    c22 = add(add(subtract(p1, p2), p3), p6)
    
    result = [[0 for j in range(0, n)] for i in range(0, n)]
    
    for i in range(0, newSize):
        for j in range(0, newSize):
            result[i][j] = a11[i][j] = c11[i][j]            # top left
            result[i][j + newSize] = c12[i][j]     # top right
            result[i + newSize][j] = c21[i][j]    # bottom left
            result[i + newSize][j + newSize] = c22[i][j]  # bottom right
    return result


    
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  
    
    
n = 8
A = [[0 for j in range(0, n)] for i in range(0, n)]
B = [[0 for j in range(0, n)] for i in range(0, n)]
fillMat(A, B, n)
print('Matrix A')
printMatrix(A, n)
print('Matrix B')
printMatrix(B, n)
#printMatrix(multiply(A,B), n)
C = strass(A, B, n, n, comm)
#print('Matrix C = AB')
#printMatrix(C, n)

