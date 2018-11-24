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
newgroup1 = group.Incl([0, 1, 2])
newgroup2 = group.Incl([3, 4, 5])
#print('in here 2 with id ' + str(rank))
newcomm1 = comm.Create(newgroup1)
newcomm2 = comm.Create(newgroup2)
#print('in here 3.5 with id ' + str(rank))
for i in range(0,7):
    if i == 0:
        if i*size <= rank <= (i+1)*size-1: 
            p1 = printGroup(newcomm1,i)
            print('in here 3 with id ' + str(rank) + ' with stored number ' + str(p1))
    if i == 1:
        if i*size <= rank <= (i+1)*size-1: 
            p1 = printGroup(newcomm2,i)
            print('in here 3 with id ' + str(rank) + ' with stored number ' + str(p1))
            

group.Free(); newgroup1.Free()
if newcomm1: newcomm1.Free()
