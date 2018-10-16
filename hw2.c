#include<mpi.h>
#include<stdio.h>
int main(int argc,char*argv[]){
    int coreId, totalCore, i;
    int messageSize = 100;
    int trial = 10;
    int message [messageSize];
    double total_my_bcast_time = 0.0;
    double total_mpi_bcast_time = 0.0;
    for( i = 0; i<messageSize; i = i+1){
        message[i] =i;
    }
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &coreId);
    MPI_Comm_size(MPI_COMM_WORLD, &totalCore);
    MPI_Request request;
    int times;
    int anotherBuffer [messageSize];
    for(times = 0; times < trial, times++){
     //my_bcast
    MPI_Barrier(MPI_COMM_WORLD);
    total_my_bcast_time -= MPI_Wtime();
    if(coreId == 0){
         int count;
         for(count = 1; count<totalCore; count = count +1){
            MPI_Send(message, messageSize, MPI_INT, count, 0, MPI_COMM_WORLD);
         }
        printf("%d message broadcasted from core %d using Send \n", messageSize, coreId);
    }
    else{
        MPI_Recv(anotherBuffer, messageSize, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("%d numbers received from core 0 by core %d using Recv\n", messageSize, coreId);  
        anotherBuffer = NULL; 
    }
    MPI_Barrier(MPI_COMM_WORLD);
    total_my_bcast_time += MPI_Wtime();

    //MPI_Bcast 
     MPI_Barrier(MPI_COMM_WORLD);
     total_mpi_bcast_time -= MPI_Wtime();
     MPI_Bcast(message, messageSize, MPI_INT, 0, MPI_COMM_WORLD);
     printf("%d numbers received from core 0 by core usng Bcast %d \n", messageSize, coreId);   
     MPI_Barrier(MPI_COMM_WORLD);
     total_mpi_bcast_time += MPI_Wtime();
    }

     if (coreId == 1) {
     printf("Data size = %d\n", messageSize);
     printf("Average MPI_Bcast time = %lf\n", total_mpi_bcast_time/trial);
     printf("Average my bcast time = %lf\n", total_my_bcast_time/trial);
  }
    MPI_Finalize();
}