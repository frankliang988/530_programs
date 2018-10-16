#include<mpi.h>
#include<stdio.h>
int main(int argc,char*argv[]){
    int coreId, totalCore;
    int messageSize = 100;
    int message [messageSize];
    for(int i = 0; i<100; i = i+1){
        message[i] = 1;
    }
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &coreId);
    MPI_Comm_size(MPI_COMM_WORLD, &totalCore);
    
    //MPI_Bcast 
    if(coreId == 0){
        MPI_Bcast(message, 100, MPI_INT, coreId+1, 0, MPI_COMM_WORLD);
        printf("message broadcasted from core %d \n", coreId);
    }
    else{
        int recBuffer = [100];
        MPI_Bcast(recBuffer, 100, MPI_INT, coreId+1, 0, MPI_COMM_WORLD);
        printf("100 numbers received from core 0 by core %d \n", coreId);
        
    }

    MPI_Finalize();
}