#include <stdio.h>
#include "mpi.h"
#include <math.h>
#include <stdlib.h>
#include <stddef.h>
#include <time.h>
#define N 26*24 //define column size or row size for a square matrix
void FileOut(char *prompt, float a[][N], int row, int col, int id);

int main(int argc, char **argv)
{
  int coreId, totalCore, counter,colSize, blockSize, dum, i, j, k, rotation;
  double exeTime = 0.0;
  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &coreId);
  MPI_Comm_size(MPI_COMM_WORLD, &totalCore);
  colSize = N;
  blockSize = colSize/totalCore; //how many rows and column to assign to each processor
  float tempA[blockSize][colSize]; //holds rows of A
  float tempB1[colSize][blockSize]; //holds cols of B
  float tempB2[colSize][blockSize];
  float multiResult[blockSize][blockSize]; //holds multiplication result 
  float finalResultPerCore[blockSize][colSize]; //stores the final result done by each core on each core.
  float C[colSize][colSize];

  MPI_Barrier(MPI_COMM_WORLD);
  exeTime -= MPI_Wtime();
  //initialization
  for(i = 0; i <blockSize; i++){
      for(j = 0; j<colSize; j++){
          tempA[i][j] = 0.0;
          tempB1[j][i] = 0.0;
          tempB2[j][i] = 0.0;
          finalResultPerCore[i][j] = 0.0;
      }
  }

  for(i = 0; i <blockSize; i++){
      for(j = 0; j<blockSize; j++){
          multiResult[i][j]=0;
      }
  }

  //matrix scattering
  if(coreId == 0){   //define matrices A, B on core 0
      float A[colSize][colSize];
      float B[colSize][colSize];
      srand ( time ( NULL));
      for(i = 0; i< colSize; i++){
          for(j=0; j<colSize; j++){
              A[i][j] = (float)rand()/RAND_MAX*2.0-1.0;
              B[i][j] = (float)rand()/RAND_MAX*2.0-1.0;
              C[i][j] = 0.0;
          }
      }
      
      for(counter = 1; counter<totalCore; counter++ ){
            if(coreId == 0){
                dum = counter*blockSize; //16
                //dividing matrix A into parcels
                for(i = dum; i<dum + blockSize; i++){  //16 ~ 31
                    for(j = 0; j<colSize; j++){
                        tempA[i-dum][j] = A[i][j];
                    }
                }
                //dividing matrix B into parcel
                for(i = dum; i<dum + blockSize; i++){  //16 ~ 31
                
                    for(j = 0; j<colSize; j++){
                        tempB1[j][i-dum] = B[j][i];
                    }
                }

                //send both parts to each other cores
                MPI_Send(&tempA,blockSize*colSize,MPI_FLOAT,counter,0,MPI_COMM_WORLD);
                MPI_Send(&tempB1,blockSize*colSize,MPI_FLOAT,counter,1,MPI_COMM_WORLD);
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
  //getting the matrices from core 0 by the rest
  for(counter =1; counter<totalCore; counter++ ){
      if(coreId == counter){
          MPI_Recv(&tempA, blockSize*colSize, MPI_FLOAT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
          MPI_Recv(&tempB1, blockSize*colSize, MPI_FLOAT, 0, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      }
      //print_results("A temp = ", tempA, blockSize, colSize, counter);
  }
 
  for(rotation = 0; rotation < totalCore; rotation++){
      //matrix multiplication in each core simutaneously
      for(i = 0; i<blockSize; i++){
          for(j = 0; j < blockSize; j++){
              for(k = 0; k < colSize; k++){
                  tempB2[k][i] = tempB1[k][i];
                  multiResult[i][j] = multiResult[i][j] + tempA[i][k] * tempB1[k][j];
              }    
          }
      }

      for(counter = 0; counter<totalCore; counter++){
          if(coreId == counter){
              //put matrix into final result matrix in each core in correct position
              int position = (rotation + counter) % totalCore;
                for(i = position * blockSize; i< position * blockSize + blockSize; i++){
                        for(j = 0; j<blockSize; j++){
                            finalResultPerCore[j][i] = multiResult[j][i - position * blockSize];
                            multiResult[j][i - position * blockSize] = 0;
                        }
                }
            
                //rotation starts, core 2 sends to core 1
                if(coreId == 0){
                     MPI_Send(&tempB2,blockSize*colSize,MPI_FLOAT,totalCore-1,2,MPI_COMM_WORLD);
                 } 
                 else if(coreId== totalCore-1){
                      MPI_Recv(&tempB1, blockSize*colSize, MPI_FLOAT, 0, 2, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                      MPI_Send(&tempB2,blockSize*colSize,MPI_FLOAT,counter-1,2,MPI_COMM_WORLD);
                 }else{
                     MPI_Recv(&tempB1, blockSize*colSize, MPI_FLOAT, counter+1, 2, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                     MPI_Send(&tempB2,blockSize*colSize,MPI_FLOAT,counter-1,2,MPI_COMM_WORLD);
                 }
                 if(coreId == 0){
                     MPI_Recv(&tempB1, blockSize*colSize, MPI_FLOAT, 1, 2, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                 } 
          }
      }
  }

  //to make sure each process has to correct final result.
  /*for(counter = 0; counter<totalCore; counter++){
      FileOut("final result = ", finalResultPerCore, blockSize, colSize, counter);
  }*/

   //gather all sections on to core 0 and form matrix C
   MPI_Gather(finalResultPerCore, colSize*blockSize, MPI_FLOAT, C,colSize*blockSize,MPI_FLOAT, 0, MPI_COMM_WORLD );
  
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

    //FileOut("B temp = ", tempB, colSize, blockSize, counter);
    MPI_Finalize();

}

void FileOut(char *prompt, float a[][N], int row, int col, int id)
{
    //FILE *file;
    //char output[] = "out.txt";
    //file = fopen(output, "w");
    int i, j;
    printf ("\n\n On core: %f, %s\n",id, prompt);
    for (i = 0; i < row; i++) {
            for (j = 0; j < col; j++) {
                    printf(" %f", a[i][j]);
                    //fprintf(file," %d",a[i][j]);
            }
            printf ("\n\n");
            //fprintf(file,"\n");
    }
    printf ("\n\n");
}
