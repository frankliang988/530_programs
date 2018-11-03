#include <stdio.h>
#include "mpi.h"
#include <math.h>
#include <stdlib.h>
#include <stddef.h>

void print_results(char *prompt, int a[][], int row, int col, int id);

int main(int argc, char **argv)
{
  int coreId, totalCore, counter,colSize, blockSize, dum, i, j;
  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &coreId);
  MPI_Comm_size(MPI_COMM_WORLD, &totalCore);
  colSize = 16*24;
  blockSize = 16;
  int tempA[colSize][blockSize]; //holds row of A
  int tempB[blockSize][colSize]; //holds cols of B
  int multiResult = [blockSize][blockSize]; //holds multiplication result 
  int finalResultPerCore[colSize][blockSize]; //stores the final result done by each core.
  if(coreId == 0){
      int A[colSize][colSize];
      int B[colSize][colSize];
      for(i = 0; i< colSize; i++){
          for(j=0; j<colSize; j++){
              A[i][j] == 1;
              B[i][j] == 2;
          }
      }
  }
  //sending the matrices from core 0 to the rest
  for(counter =1; counter<totalCore; counter++ ){
      if(coreId == 0){
          dum = counter*blockSize; //16
          //dividing matrix A into parcel
          for(i = dum; i<dum + blockSize; i++){  //16 ~ 31
            for(j = 0; j<colSize; j++){
                tempA[i-dum][j] = A[i][j];
            }
          }
          //dividing matrix B into parcel
          for(i = dum; i<dum + blockSize; i++){  //16 ~ 31
            for(j = 0; j<colSize; j++){
                tempB[j][i-dum] = B[j][i];
            }
          }
          MPI_Send(&tempA,blockSize*colSize,MPI_Int,counter,0,MPI_COMM_WORLD)
          MPI_Send(&tempB,blockSize*colSize,MPI_Int,counter,1,MPI_COMM_WORLD)
      }
      if(coreId == counter){
          MPI_Recv(&tempA, blockSize*colSize, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      }
      if(coreId == counter){
          MPI_Recv(&tempB, blockSize*colSize, MPI_INT, 0, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      }
      if(counter == totalCore-1){
          if(coreId == 0){
              for(i=0; i<blockSize; i++){
                  for(j = 0; j<colSize; j++){
                      tempA[i][j] = A[i][j];
                      tempB[j][i] = B[j][i];
                  }
              }
          }
      }
  }
    print_results("A temp = ", tempA, blockSize, colSize, counter);
    print_results("B temp = ", tempB, colSize, blockSize, counter);
    MPI_Finalize();

}

void print_results(char *prompt, int a[][], int row, int col, int id)
{
    int i, j;
    printf ("\n\n On core: %d, %s\n",id, prompt);
    for (i = 0; i < row; i++) {
            for (j = 0; j < col; j++) {
                    printf(" %d", a[i][j]);
            }
            printf ("\n");
    }
    printf ("\n\n");
}

