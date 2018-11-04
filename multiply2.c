#include <stdio.h>
#include "mpi.h"
#include <math.h>
#include <stdlib.h>
#include <stddef.h>
#define N 16*24

void FileOut(char *prompt, int a[][N], int row, int col, int id);

int main(int argc, char **argv)
{
  int coreId, totalCore, counter,colSize, blockSize, dum, i, j, k;
  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &coreId);
  MPI_Comm_size(MPI_COMM_WORLD, &totalCore);
  colSize = N;
  blockSize = colSize/totalCore; //how many rows and column to assign to each processor
  int tempA[blockSize][colSize]; //holds rows of A
  
  int finalResultPerCore[blockSize][colSize]; //stores the final result done by each core on each core.
  
  int C[colSize][colSize];
  
  for(i = 0; i <blockSize; i++){
      for(j = 0; j<colSize; j++){
          tempA[i][j] = 0;
          finalResultPerCore[i][j] = 0;
      }
  }

  int B[colSize][colSize];
  for(i = 0; i< colSize; i++){
          for(j=0; j<colSize; j++){
              B[i][j] = 2;
          }
   }

  if(coreId == 0){   //define matrices A, B on core 0
      int A[colSize][colSize];
      
      for(i = 0; i< colSize; i++){
          for(j=0; j<colSize; j++){
              A[i][j] = 1;
              C[i][j] = 0;
          }
      }

      for(counter =1; counter<totalCore; counter++ ){
            if(coreId == 0){
                dum = counter*blockSize; //16
                //dividing matrix A into parcels
                for(i = dum; i<dum + blockSize; i++){  //16 ~ 31
                    for(j = 0; j<colSize; j++){
                        tempA[i-dum][j] = A[i][j];
                    }
                }

                //scatter A
                MPI_Send(&tempA,blockSize*colSize,MPI_INT,counter,0,MPI_COMM_WORLD);
                if(counter == totalCore-1){ //at last, fill the parcel in A
                    if(coreId == 0){
                        for(i=0; i<blockSize; i++){
                            for(j = 0; j<colSize; j++){
                                tempA[i][j] = A[i][j];
                            }
                        }
                    }
                }
            }
      }

  }
  //getting the matrices from core 0 by the rest
  for(counter =1; counter<totalCore; counter++ ){
      if(coreId == counter){
          MPI_Recv(&tempA, blockSize*colSize, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      }
  }

  for(i = 0; i<blockSize; i++){
          for(j = 0; j < colSize; j++){
              for(k = 0; k < colSize; k++){
                  finalResultPerCore[i][j] = finalResultPerCore[i][j] + tempA[i][k] * B[k][j];
              }    
          }
      }


    MPI_Gather(finalResultPerCore, colSize*blockSize, MPI_INT, C,colSize*blockSize,MPI_INT, 0, MPI_COMM_WORLD );
  
   //output final result to a text file.
   if(coreId == 0){
       FileOut("C = ", C, colSize, colSize, 0);
   }
    MPI_Finalize();
}

void FileOut(char *prompt, int a[][N], int row, int col, int id)
{
    FILE *file;
    char output[] = "out.txt";
    file = fopen(output, "w");
    int i, j;
    printf ("\n\n On core: %d, %s\n",id, prompt);
    for (i = 0; i < row; i++) {
            for (j = 0; j < col; j++) {
                    printf(" %d", a[i][j]);
                    fprintf(file," %d",a[i][j]);
            }
            printf ("\n");
            fprintf(file,"\n");
    }
    printf ("\n\n");
}