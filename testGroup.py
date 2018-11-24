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

comm = MPI.COMM_WORLD
rank = comm.Get_rank() 
size = comm.Get_size()//7

for i in range(0,7):
    if i == 0:
        if i*size <= rank <= (i+1)*size-1:
            group = comm.Get_group()
            print('in here 1 with id ' + str(rank))
            newgroup = group.Incl([0, 1, 2])
            print('in here 2 with id ' + str(rank))
            newcomm = comm.Create(newgroup)
            print('in here 3.5 with id ' + str(rank))
            printGroup(newcomm,i)
            print('in here 3 with id ' + str(rank))
            group.Free(); newgroup.Free()
            if newcomm: newcomm.Free()
    if i == 1:
        if i*size <= rank <= (i+1)*size-1:
            group = comm.Get_group()
            newgroup = group.Incl([3, 4, 5])
            newcomm = comm.Create(newgroup)
            printGroup(newcomm,i)
            group.Free(); newgroup.Free()
            if newcomm: newcomm.Free()

