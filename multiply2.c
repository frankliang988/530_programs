#include <stdio.h>
#include "mpi.h"
#include <math.h>
#include <stdlib.h>
#include <stddef.h>
#include <time.h>
#define N 16*24

void FileOut(char *prompt, double a[][N], int row, int col, int id);

int main(int argc, char **argv)
{
  int coreId, totalCore, counter,colSize, blockSize, dum, i, j, k;
   double exeTime = 0.0;
   srand ( time ( NULL));
   //generate B
   double B[colSize][colSize];
    for(i = 0; i< colSize; i++){
          for(j=0; j<colSize; j++){
              //B[i][j] = i+j;   // testing matrix
              B[i][j] = (double)rand()/RAND_MAX*2.0-1.0;
          }
   }
  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &coreId);
  MPI_Comm_size(MPI_COMM_WORLD, &totalCore);
  colSize = N;
  blockSize = colSize/totalCore; //how many rows and column to assign to each processor
  double tempA[blockSize][colSize]; //holds rows of A
  
  double finalResultPerCore[blockSize][colSize]; //stores the final result done by each core on each core.
  
  MPI_Barrier(MPI_COMM_WORLD);
  exeTime -= MPI_Wtime();
  for(i = 0; i <blockSize; i++){
      for(j = 0; j<colSize; j++){
          tempA[i][j] = 0;
          finalResultPerCore[i][j] = 0;
      }
  }

  if(coreId == 0){   //define matrices A, B on core 0
      double A[colSize][colSize];
      
      for(i = 0; i< colSize; i++){
          for(j=0; j<colSize; j++){
              //A[i][i] = 1;   //identity matrix for testing
              A[i][j] = (double)rand()/RAND_MAX*2.0-1.0;
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
                MPI_Send(&tempA,blockSize*colSize,MPI_DOUBLE,counter,0,MPI_COMM_WORLD);
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
          MPI_Recv(&tempA, blockSize*colSize, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      }
  }

  for(i = 0; i<blockSize; i++){
          for(j = 0; j < colSize; j++){
              for(k = 0; k < colSize; k++){
                  finalResultPerCore[i][j] = finalResultPerCore[i][j] + tempA[i][k] * B[k][j];
              }    
          }
      }


    MPI_Gather(finalResultPerCore, colSize*blockSize, MPI_DOUBLE, C,colSize*blockSize,MPI_DOUBLE, 0, MPI_COMM_WORLD );
  
   //output final result to a text file.
   if(coreId == 0){
       FileOut("C = ", C, colSize, colSize, 0);
   }
   MPI_Barrier(MPI_COMM_WORLD);
   exeTime += MPI_Wtime();
   if(coreId == 0){
       printf("Matrix size: %d by %d on %d cores:\n", N, N, totalCore);
       printf("Mat mutiply execution time = %lf\n", exeTime);
   }
    MPI_Finalize();
}

void FileOut(char *prompt, double a[][N], int row, int col, int id)
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