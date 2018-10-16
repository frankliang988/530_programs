#include<mpi.h>
#include<stdio.h>
int main(int argc,char*argv[]){
    int coreId, totalCore;
    int message = 1;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &coreId);
    MPI_Comm_size(MPI_COMM_WORLD, &totalCore);
    
    if(coreId == 0){
        printf("Hello from %d of total %d cores \n", coreId, totalCore);
        MPI_Send(&message, 1, MPI_INT, coreId+1, 0, MPI_COMM_WORLD);
    }
    else{
        int recBuffer;
        MPI_Recv(&recBuffer, 1, MPI_INT, coreId-1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("Hello from %d of total %d cores \n", coreId, totalCore);
        if(coreId < totalCore - 1){
           MPI_Send(&message, 1, MPI_INT, coreId+1, 0, MPI_COMM_WORLD); 
        }
    }
    MPI_Finalize();
}