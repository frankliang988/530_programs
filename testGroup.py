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
        if i*size <= id <= (i+1)*size-1:
            group = comm.Get_group()
            newgroup = group.Incl(range(i*size, (i+1)*size))
            newcomm = comm.Create(newgroup)
            printGroup(newcomm,i)
            group.Free(); newgroup.Free()
            if newcomm: newcomm.Free()
    if i == 1:
        if i*size <= id <= (i+1)*size-1:
            group = comm.Get_group()
            newgroup = group.Incl(range(i*size, (i+1)*size))
            newcomm = comm.Create(newgroup)
            printGroup(newcomm,i)
            group.Free(); newgroup.Free()
            if newcomm: newcomm.Free()

