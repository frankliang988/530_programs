#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 19:41:53 2018

@author: frankliang
"""

from mpi4py import MPI

def printGroup(comm, id):
    id = comm.Get_rank()
    size = comm.Get_size()
    print('core %d '+str(id)+ ' in group '+ str(id) + ' with ' + str(size) + 'cores in group')
    return 3

comm = MPI.COMM_WORLD
rank = comm.Get_rank() 
size = comm.Get_size()//7
group = comm.Get_group()
#print('in here 1 with id ' + str(rank))
newgroup1 = group.Incl(list(range(0*size,1*size)))
newgroup2 = group.Incl(list(range(1*size,2*size)))
newgroup3 = group.Incl(list(range(2*size,3*size)))
newgroup4 = group.Incl(list(range(3*size,4*size)))
newgroup5 = group.Incl(list(range(4*size,5*size)))
newgroup6 = group.Incl(list(range(5*size,6*size)))
newgroup7 = group.Incl(list(range(6*size,7*size)))
#print('in here 2 with id ' + str(rank))
newcomm1 = comm.Create(newgroup1)
newcomm2 = comm.Create(newgroup2)
newcomm3 = comm.Create(newgroup3)
newcomm4 = comm.Create(newgroup4)
newcomm5 = comm.Create(newgroup5)
newcomm6 = comm.Create(newgroup6)
newcomm7 = comm.Create(newgroup7)

#print('in here 3.5 with id ' + str(rank))
for i in range(0,7):
    if i == 0:
        if i*size <= rank <= (i+1)*size-1: 
            p1 = printGroup(newcomm1,i)
            #print('in here 3 with id ' + str(rank) + ' with stored number ' + str(p1))
    if i == 1:
        if i*size <= rank <= (i+1)*size-1: 
            p1 = printGroup(newcomm2,i)
            #print('in here 3 with id ' + str(rank) + ' with stored number ' + str(p1))
    if i == 2:
        if i*size <= rank <= (i+1)*size-1: 
            p1 = printGroup(newcomm2,i)
            #print('in here 3 with id ' + str(rank) + ' with stored number ' + str(p1))
    if i == 3:
        if i*size <= rank <= (i+1)*size-1: 
            p1 = printGroup(newcomm2,i)
            #print('in here 3 with id ' + str(rank) + ' with stored number ' + str(p1))
    if i == 4:
        if i*size <= rank <= (i+1)*size-1: 
            p1 = printGroup(newcomm2,i)
            #print('in here 3 with id ' + str(rank) + ' with stored number ' + str(p1))
    if i == 5:
        if i*size <= rank <= (i+1)*size-1: 
            p1 = printGroup(newcomm2,i)
            #print('in here 3 with id ' + str(rank) + ' with stored number ' + str(p1))
    if i == 6:
        if i*size <= rank <= (i+1)*size-1: 
            p1 = printGroup(newcomm2,i)
            #print('in here 3 with id ' + str(rank) + ' with stored number ' + str(p1))
            

group.Free(); newgroup1.Free()
newgroup2.Free()
newgroup3.Free()
newgroup4.Free()
newgroup5.Free()
newgroup6.Free()
newgroup7.Free()
if newcomm1: newcomm1.Free()
if newcomm2: newcomm2.Free()
if newcomm3: newcomm3.Free()
if newcomm4: newcomm4.Free()
if newcomm5: newcomm5.Free()
if newcomm6: newcomm6.Free()
if newcomm7: newcomm7.Free()
