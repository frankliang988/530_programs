#include<mpi.h>
#include<stdio.h>
int main(int argc,char*argv[]){
    int coreId, totalCore;
    int message = 1;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &coreId);
    MPI_Comm_size(MPI_COMM_WORLD, &totalCore);
    int counter = 0;
    
    if(coreId == totalCore){
        printf("Hello from %d of total %d cores \n", coreId, totalCore);
        MPI_Send(&message, 1, MPI_INT, coreId-1, 0, MPI_COMM_WORLD);
        counter ++;
    }
    else{
        int recBuffer;
        MPI_Recv(&number, 1, MPI_INT, coreId+1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("Hello from %d of total %d cores \n", coreId, totalCore);
        if(coreId>0){
           MPI_Send(&message, 1, MPI_INT, coreId-1, 0, MPI_COMM_WORLD); 
        }
    }
    MPI_Finalize()
}