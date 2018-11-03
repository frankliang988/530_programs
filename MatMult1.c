#include <stdio.h>
#include "mpi.h"
#include <math.h>
#include <stdlib.h>
#include <stddef.h>
#define N 16*24
void print_results(char *prompt, int a[][], int row, int col, int id);

int main(int argc, char **argv)
{
  int coreId, totalCore, counter,colSize, blockSize, dum, i, j, k, rotation, sum = 0;
  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &coreId);
  MPI_Comm_size(MPI_COMM_WORLD, &totalCore);
  colSize = 16*24;
  blockSize = 16;
  int tempA[blockSize][colSize] = {0}; //holds row of A
  int tempB[colSize][blockSize] = {0}; //holds cols of B
  int multiResult[blockSize][blockSize] = {0}; //holds multiplication result 
  int finalResultPerCore[colSize][blockSize] = {0}; //stores the final result done by each core.

  //matrix scattering
  if(coreId == 0){  
      int A[colSize][colSize];
      int B[colSize][colSize];
      for(i = 0; i< colSize; i++){
          for(j=0; j<colSize; j++){
              A[i][j] == 1;
              B[i][j] == 2;
          }
      }

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

                //send both parts to all other cored
                MPI_Send(&tempA,blockSize*colSize,MPI_INT,counter,0,MPI_COMM_WORLD);
                MPI_Send(&tempB,blockSize*colSize,MPI_INT,counter,1,MPI_COMM_WORLD);
                if(counter == totalCore-1){ //at last, fill the parcel in A
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
      }
  }
  //getting the matrices from core 0 to the rest
  for(counter =1; counter<totalCore; counter++ ){
      if(coreId == counter){
          MPI_Recv(&tempA, blockSize*colSize, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
          MPI_Recv(&tempB, blockSize*colSize, MPI_INT, 0, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      }
      print_results("A temp = ", tempA, blockSize, colSize, counter);
  }
 
  for(rotation = 0; rotation < totalCore; rotation++){
      //matrix multiplication in each core simutaneously
      for(i = 0; i<blockSize; i++){
          for(j = 0; j < blockSize; j++){
              for(k = 0; k < colSize; k++){
                  multiResult[i][j] = multiResult[i][j] + tempA[i][k] * tempB[k][j];
              }    
          }
      }

      for(counter = 0; counter<totalCore; counter++){
          if(coreId == counter){
              //put matrix into final result matrix in each core in correct position
              int position = (rotation + counter) % totalCore;
              int rot = (counter+1) % totalCore
                for(i = position * blockSize; i< position * blockSize + blockSize; i++){
                        for(j = 0; j<blockSize; j++){
                            finalResultPerCore[i][j] = multiResult[i - position * blockSize][j];
                        }
                }
            
                //rotation starts, core 2 sends to core 1
                if(counter != 0){
                    MPI_Send(&tempB,blockSize*colSize,MPI_INT,counter-1,2,MPI_COMM_WORLD);
                } else{
                    MPI_Send(&tempB,blockSize*colSize,MPI_INT,totalCore-1,2,MPI_COMM_WORLD);
                }
                MPI_Recv(&tempB, blockSize*colSize, MPI_INT, rot, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                  
          }
      }
  }

  for(counter = 0; counter<totalCore; counter++){
      print_results("final result = ", finalResultPerCore, blockSize, colSize, counter);
  }









    //print_results("B temp = ", tempB, colSize, blockSize, counter);
    MPI_Finalize();

}

void print_results(char *prompt, int a[][N], int row, int col, int id)
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

