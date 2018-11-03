#include<mpi.h>
#include<stdio.h>
int main(int argc,char*argv[]){
    int coreId, totalCore, i;
    int messageSize = 100; //number of numbers to send, change this number to send message of different size
    int trial = 10;
    int message [messageSize];
    double total_my_bcast_time = 0.0;
    double total_mpi_bcast_time = 0.0;
    //initialize the message
    for( i = 0; i<messageSize; i = i+1){
        message[i] =i;
    }
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &coreId);
    MPI_Comm_size(MPI_COMM_WORLD, &totalCore);
    //MPI_Request request;
    int times; //a simple counter for the trials
    int anotherBuffer [messageSize];
    for(times = 0; times < trial; times++){ //run 10 trials and collect the average
     //my_bcast
    MPI_Barrier(MPI_COMM_WORLD);
    total_my_bcast_time -= MPI_Wtime();
    if(coreId == 0){
         int count;
         //send the message to the rest of the cores
         for(count = 1; count<totalCore; count = count +1){
            MPI_Send(message, messageSize, MPI_INT, count, 0, MPI_COMM_WORLD);
         }
        //printf("%d message broadcasted from core %d using Send \n", messageSize, coreId);
    }
    else{
        //get message from core 0
        MPI_Recv(anotherBuffer, messageSize, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        //printf("%d numbers received from core 0 by core %d using Recv\n", messageSize, coreId);  
    }
    MPI_Barrier(MPI_COMM_WORLD);
    total_my_bcast_time += MPI_Wtime();

    //MPI_Bcast 
     MPI_Barrier(MPI_COMM_WORLD);
     total_mpi_bcast_time -= MPI_Wtime();
     //invoke mpi_bcast on all cores
     MPI_Bcast(message, messageSize, MPI_INT, 0, MPI_COMM_WORLD);
     //printf("%d numbers received from core 0 by core usng Bcast %d \n", messageSize, coreId);   
     MPI_Barrier(MPI_COMM_WORLD);
     total_mpi_bcast_time += MPI_Wtime();
    }

     if (coreId == 1) {
     printf("Data size = %d\n", messageSize);
     //mpi_bcast average speed of 10 trials
     printf("Average MPI_Bcast time = %lf\n", total_mpi_bcast_time/trial);
     //my bcast speed of 10 trials
     printf("Average my bcast time = %lf\n", total_my_bcast_time/trial);
  }
    MPI_Finalize();
}