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

def multiply(A, B, comm):
    id = comm.Get_rank()
    size = comm.Get_size()
    n = len(A)
    blockSize = n//2
    C = [[0 for j in range(0, n)] for i in range(0, blockSize)]
    result1 = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0,size):
        if id == i:
            for i in range(0, blockSize):
                for j in range(0, n):
                    for k in range(0, n):
                        C[i][j] = C[i][j] + A[i][k] * B[k][j]
            if id != 0:
                comm.send(C, dest=0, tag = 12)
    
    if id ==0:
        for i in range(1,size):
            d = comm.recv(source = i, tag = 12)
            for j in range(0, blockSize):
                for k in range(0, n):
                    result1[j+i*blockSize][k] = d[j][k] 
        for j in range(0, blockSize):
            for k in range(0, n):
                result1[j][k] = C[j][k] 
            
    result = comm.bcast(result1, root = 0)
    
    return result

def strass(A, B, n, total, communicator):
    #determines the number of recursion, //2 for 1st lvl, //4 for 2nd, //8 for 3rd
    if n == total//2:
        return multiply(A, B, communicator)
    
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
        size = communicator.Get_size()//7
        group = communicator.Get_group()
        result1 = [[0 for j in range(0, n)] for i in range(0, n)]
        newgroup1 = group.Incl(range(0*size,1*size))
        newgroup2 = group.Incl(range(1*size,2*size))
        newgroup3 = group.Incl(range(2*size,3*size))
        newgroup4 = group.Incl(range(3*size,4*size))
        newgroup5 = group.Incl(range(4*size,5*size))
        newgroup6 = group.Incl(range(5*size,6*size))
        newgroup7 = group.Incl(range(6*size,7*size))
        newcomm1 = comm.Create(newgroup1)
        newcomm2 = comm.Create(newgroup2)
        newcomm3 = comm.Create(newgroup3)
        newcomm4 = comm.Create(newgroup4)
        newcomm5 = comm.Create(newgroup5)
        newcomm6 = comm.Create(newgroup6)
        newcomm7 = comm.Create(newgroup7)
        p1 = result1
        p2 = result1
        p3 = result1
        p4 = result1
        p5 = result1
        p6 = result1
        p7 = result1
        for i in range(0,7):
            if i == 0:
                if i*size <= id < (i+1)*size:
                    p1 = strass(add(a11, a22), add(b11, b22), newSize, total,newcomm1)
                    newgroup1.Free()
                    if newcomm1: newcomm1.Free()
            elif i == 1:
                if i*size <= id < (i+1)*size:
                    p2 = strass(add(a21, a22), b11, newSize, total,newcomm2)
                    #if id == i:
                        #communicator.send(p2, dest=0, tag = 1)
                    newgroup2.Free()
                    if newcomm2: newcomm2.Free()
            elif i == 2:
                if i*size <= id < (i+1)*size:
                    p3 = strass(a11, subtract(b12, b22), newSize, total,newcomm3)
                    #if id == i:
                        #communicator.send(p3, dest=0, tag = 1)
                    newgroup3.Free()
                    if newcomm3: newcomm3.Free()
            elif i == 3:
                if i*size <= id < (i+1)*size:
                    p4 = strass(a22, subtract(b21, b11), newSize, total,newcomm4)
                    #if id == i:
                        #communicator.send(p4, dest=0, tag = 1)
                    newgroup4.Free()
                    if newcomm4: newcomm4.Free()
            elif i == 4:
                if i*size <= id < (i+1)*size:
                    p5 = strass(add(a11, a12),b22, newSize, total,newcomm5)
                    #if id == i:
                        #communicator.send(p5, dest=0, tag = 1)
                    newgroup5.Free()
                    if newcomm5: newcomm5.Free()
            elif i == 5:
                if i*size <= id < (i+1)*size:
                    p6 = strass(subtract(a21, a11), add(b11, b12), newSize, total,newcomm6)
                    #if id == i:
                        #communicator.send(p6, dest=0, tag = 1)
                    newgroup6.Free()
                    if newcomm6: newcomm6.Free()
            elif i == 6:
                if i*size <= id < (i+1)*size:
                    p7 = strass(subtract(a12, a22), add(b21, b22), newSize, total,newcomm7)
                    #if id == i:
                        #communicator.send(p7, dest=0, tag = 1)
                    newgroup7.Free()
                    if newcomm7: newcomm7.Free()
        group.Free()
        for i in range(0,7):
            if i == 1:
                if id == i:
                    communicator.send(p2, dest=0, tag = 1)
            if i == 2:
                if id == i:
                    communicator.send(p3, dest=0, tag = 1)
            if i == 3:
                if id == i:
                    communicator.send(p4, dest=0, tag = 1)
            if i == 4:
                if id == i:
                    communicator.send(p5, dest=0, tag = 1)
            if i == 5:
                if id == i:
                    communicator.send(p6, dest=0, tag = 1)
            if i == 6:
                if id == i:
                    communicator.send(p7, dest=0, tag = 1)
    
        if id == 0:
            #p1 = A
            p2 = communicator.recv(source = 1, tag = 1)
            p3 = communicator.recv(source = 2, tag = 1)
            p4 = communicator.recv(source = 3, tag = 1)
            p5 = communicator.recv(source = 4, tag = 1)
            p6 = communicator.recv(source = 5, tag = 1)
            p7 = communicator.recv(source = 6, tag = 1)
            
            c11 = add(subtract(add(p1, p4),p5), p7)
            c12 = add(p3, p5)
            c21 = add(p2, p4)
            c22 = add(add(subtract(p1, p2), p3), p6)
            
    
            for i in range(0, newSize):
                for j in range(0, newSize):
                    result1[i][j] = a11[i][j] = c11[i][j]            # top left
                    result1[i][j + newSize] = c12[i][j]     # top right
                    result1[i + newSize][j] = c21[i][j]    # bottom left
                    result1[i + newSize][j + newSize] = c22[i][j]  # bottom right
            #for i in range(1,size):
                #communicator.send(result1, dest=i, tag = 2)
        
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

