# -*- coding: utf-8 -*-
"""
Paralled Matrix multiplication using strassen algorithm via MPI

Author: Frank Liang
"""
from mpi4py import MPI

#fill up testing matrices
def fillMat(A, B, n):
    for i in range(n):
        for j in range(n):
            A[i][j]= i+j;
            if i == j:
                B[i][j] = 2
            else:
                B[i][j] = 0
    return A, B

#function for printing matrices
def printMatrix(matrix, n):
    for i in range(n):
        for j in range(n):
            print(matrix[i][j], end=' ')
        print()

#adding 2 matrices      
def add(A, B):
    n = len(A)
    C = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            C[i][j] = A[i][j] + B[i][j]
    return C

#subtract 2 matrices
def subtract(A, B):
    n = len(A)
    C = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range(0, n):
        for j in range(0, n):
            C[i][j] = A[i][j] - B[i][j]
    return C

#multiplying matrices using basic parallel method
def multiply(A, B, comm):
    #get the comm size
    id = comm.Get_rank()
    size = comm.Get_size()
    n = len(A)
    #blocsize: how many rows should be handled to each cores within the com
    blockSize = n//size
    C = [[0 for j in range(0, n)] for i in range(0, blockSize)]
    result1 = [[0 for j in range(0, n)] for i in range(0, n)]
    #matrix mutiplication on each core
    for s in range(0,size):
        if id == s:
            for i in range(0, blockSize):
                for j in range(0, n):
                    for k in range(0, n):
                        C[i][j] = C[i][j] + A[i+s*blockSize][k] * B[k][j]
            #sending the result to the 0 core in each comm
            if id != 0:
                comm.send(C, dest=0, tag = 12)
    
    if id ==0:
        #print('in here A')
        #printMatrix(A,n)
        #print('in here B')
        #printMatrix(B,n)
        #print('in here C')
        #printMatrix(C,n)
        
        #receive and place each data in correct final result position
        for i in range(1,size):
            d = comm.recv(source = i, tag = 12)
            for j in range(0, blockSize):
                for k in range(0, n):
                    result1[j+i*blockSize][k] = d[j][k] 
        for j in range(0, blockSize):
           for k in range(0, n):
                result1[j][k] = C[j][k] 
      #brocast to each other core so every core can return the result due
      #to the nature of recursive function
    result = comm.bcast(result1, root = 0)
    
    return result


#strass mat multiplication call
def strass(A, B, n, total, communicator):
    #determines the number of recursion, //2 for 1st lvl, //4 for 2nd, //8 for 3rd
    
    #base case, when n == total//8 for the 3rd level of recursive call
    if n == total//8:
        return multiply(A, B, communicator)
    
    #else.... proceed
    
    #divie matrices A,B, two n by n matrices into eight n/2 by n/2 matrices
    newSize = n//2
    a11 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
    a12 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
    a21 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
    #dum = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
    a22 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]

    b11 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
    b12 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
    b21 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
    b22 = [[0 for j in range(0, newSize)] for i in range(0, newSize)]
    
    #initialize the 8 small matrices
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
    
    #at the 2nd last level of recursive call, parallelization occurs
    if n == total//4:
        
        id = communicator.Get_rank()
        #size = # of cores in each group, there are 7 groups
        size = communicator.Get_size()//7
        group = communicator.Get_group()
        
        result1 = [[0 for j in range(0, n)] for i in range(0, n)]
        
        #divie the cores into 7 groups, and create 7 MPI_Comm from the groups
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
        
        #TODO: fix this part as it is not really required
        #p1 = dum
        #p2 = dum
        #p3 = dum
        #p4 = dum
        #p5 = dum
        #p6 = dum
        #p7 = dum
        for i in range(0,7):
            #each group handles base case of mat multiplication
            #1st core in each group sends the result to core 0 of the
            #MPI_WORLD_COMM, then free the group and the comm used by the group
            if i == 0:
                if i*size <= id < (i+1)*size:
                    p1 = strass(add(a11, a22), add(b11, b22), newSize, total,newcomm1)
                    #if id == i*size:
                        #print('p1')
                       # printMatrix(p1,newSize)
                    newgroup1.Free()
                    if newcomm1: newcomm1.Free()
            elif i == 1:
                if i*size <= id < (i+1)*size:
                    p2 = strass(add(a21, a22), b11, newSize, total,newcomm2)
                    if id == i*size:
                        communicator.send(p2, dest=0, tag = 1)
                    #if id == i*size:
                        #print('p2')
                       # printMatrix(p2,newSize)
                    newgroup2.Free()
                    if newcomm2: newcomm2.Free()
            elif i == 2:
                if i*size <= id < (i+1)*size:
                    p3 = strass(a11, subtract(b12, b22), newSize, total,newcomm3)
                    if id == i*size:
                        communicator.send(p3, dest=0, tag = 1)
                    #if id == i*size:
                        #print('p3')
                       # printMatrix(p3,newSize)
                    newgroup3.Free()
                    if newcomm3: newcomm3.Free()
            elif i == 3:
                if i*size <= id < (i+1)*size:
                    p4 = strass(a22, subtract(b21, b11), newSize, total,newcomm4)
                    if id == i*size:
                        communicator.send(p4, dest=0, tag = 1)
                    #if id == i*size:
                        #print('p4')
                       # printMatrix(p4,newSize)
                    newgroup4.Free()
                    if newcomm4: newcomm4.Free()
            elif i == 4:
                if i*size <= id < (i+1)*size:
                    p5 = strass(add(a11, a12),b22, newSize, total,newcomm5)
                    if id == i*size:
                        communicator.send(p5, dest=0, tag = 1)
                    #if id == i*size:
                        #print('p5')
                       # printMatrix(p5,newSize)
                    newgroup5.Free()
                    if newcomm5: newcomm5.Free()
            elif i == 5:
                if i*size <= id < (i+1)*size:
                    p6 = strass(subtract(a21, a11), add(b11, b12), newSize, total,newcomm6)
                    if id == i*size:
                        communicator.send(p6, dest=0, tag = 1)
                    #if id == i*size:
                        #print('p6')
                       # printMatrix(p6,newSize)
                    newgroup6.Free()
                    if newcomm6: newcomm6.Free()
            elif i == 6:
                if i*size <= id < (i+1)*size:
                    p7 = strass(subtract(a12, a22), add(b21, b22), newSize, total,newcomm7)
                    if id == i*size:
                        communicator.send(p7, dest=0, tag = 1)
                    #if id == i*size:
                        #print('p7')
                       # printMatrix(p7,newSize)
                    newgroup7.Free()
                    if newcomm7: newcomm7.Free()
        group.Free()
        #for i in range(0,7):
            #if i == 1:
                #if id == i*size:
                    #communicator.send(p2, dest=0, tag = 1)
            #if i == 2:
                #if id == i*size:
                    #communicator.send(p3, dest=0, tag = 1)
            #if i == 3:
                #if id == i*size:
                    #communicator.send(p4, dest=0, tag = 1)
            #if i == 4:
                #if id == i*size:
                    #communicator.send(p5, dest=0, tag = 1)
            #if i == 5:
                #if id == i*size:
                    #communicator.send(p6, dest=0, tag = 1)
            #if i == 6:
                #if id == i*size:
                    #communicator.send(p7, dest=0, tag = 1)
    
        if id == 0:
            #p1 = A
            #receive all the results by core 0
            p2 = communicator.recv(source = 1*size, tag = 1)
            p3 = communicator.recv(source = 2*size, tag = 1)
            p4 = communicator.recv(source = 3*size, tag = 1)
            p5 = communicator.recv(source = 4*size, tag = 1)
            p6 = communicator.recv(source = 5*size, tag = 1)
            p7 = communicator.recv(source = 6*size, tag = 1)
            
            #calculate the four parts of A*B
            c11 = add(subtract(add(p1, p4),p5), p7)
           # print('c11 = 1+4-5+7')
           # printMatrix(c11,newSize)
            c12 = add(p3, p5)
           # print('c12 = 3+5')
           # printMatrix(c12,newSize)
            c21 = add(p2, p4)
           # print('c21 = 2+5')
           # printMatrix(c21,newSize)
            c22 = add(add(subtract(p1, p2), p3), p6)
           # print('c22 = 1-2+3+6')
           # printMatrix(c22,newSize)
            
           #putting the four parts in the correct place
            for i in range(0, newSize):
                for j in range(0, newSize):
                    result1[i][j] = a11[i][j] = c11[i][j]            
                    result1[i][j + newSize] = c12[i][j]    
                    result1[i + newSize][j] = c21[i][j]    
                    result1[i + newSize][j + newSize] = c22[i][j]  
            #for i in range(1,size):
                #communicator.send(result1, dest=i, tag = 2)
        #bcast teh final result to all cores due to the recurssive nature of the problem
        result = communicator.bcast(result1, root = 0)
        #print('Matrix C = AB')
        #printMatrix(result, n)
        return result;
        
        
    #if it is not the base case or the 2nd to last level of recursive call,
    #proceed with usual strassen algorithm    
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
#strass function ends

 # main class starts here   
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  
    
#n = row size of matrices A,B, n >= #of cores / 7 * 8 for the program to work
#with 3 levels of recusive call. i.e: for 14 cores, n has to be at least 16

#size of the matrix, has to be at least 8*totalCore/7*s where s = 1,2.....
#if n works for 112 cores, it will also work fore 56,28,7, 14....etc cores
n = 256 
 
A = [[0 for j in range(0, n)] for i in range(0, n)]
B = [[0 for j in range(0, n)] for i in range(0, n)]

#fill testing matrices
fillMat(A, B, n)

#printMatrix(multiply(A,B), n)
#call strassen
comm.barrier()
wt = MPI.Wtime()
C = strass(A, B, n, n, comm)
wt = MPI.Wtime() - wt
if rank == 0:
    print('Matrix A')
    printMatrix(A, n)
    print('Matrix B')
    printMatrix(B, n)
    print('Matrix C = AB')
    printMatrix(C, n)
    print('Total execution time: ' + str(wt) + 'sec')
    

