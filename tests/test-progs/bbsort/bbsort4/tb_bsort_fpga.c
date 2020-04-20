// Written by Ajumal NITK
#include "bsort100.h"
#include <cstdio>
#include <new>
#include <unistd.h>
#include <stdint.h>

using namespace std;
int number_array[20];//Read Area
unsigned long long* p0;

int main()
{
	int n = 25;
   int number_array[n+3] = {1,2,200,10,34,65,23,78,79,11,23,55,123,1001,91,11221,1,7,203020,12,
   2028,2010};
   int i;
   printf("------Original Array-------\n");
   for(i=0; i<n; i++)
   {
	 printf("%d \n", number_array[i]);
	}

	p0 =(unsigned long long *) new((unsigned long long *)0xc0000000) unsigned long long[10];//Contro Port
	/* old method of waiting for FPGA
	while(1){
		while(p0[8]);
		p0[0] = getpid()*getpid();
		p0[8] = 1;//Try to Occupy the FPGA
		if (p0[0] == getpid()*getpid()) break;//Occupy the FPGA Successfully
		// Two processes might try to control the FPGA at the same time which might turn
		// to the situation that two processes occupy the FPGA at the same time. These lines will prevent
		// the simulation from this error.
	} */
	// new method after implementing TaskHashes queue in fpga
	uint32_t size = n;
	uint32_t pid = getpid()*getpid();
	uint64_t r =0;
	r=r| pid;
	r=r<<32;
	r=r|size;
	p0[0] = r;
	// p0[13] = 0; 	
	printf("p00=%lu      pid=%lu    what=%d\n",p0[0],getpid()*getpid(), (p0[0] == getpid()*getpid()) );
	while(p0[0] != getpid()*getpid()); // Wait for FPGA
	p0[8] = 1;// Try to occupy the FPGA
	p0[1] = (unsigned long long)number_array;//ReadBase
	p0[2] = (unsigned long long)number_array;//WriteBase
	p0[3] = getpid();//CurrentThreadID
	p0[4] = 31;//Memory Range
	p0[5] = 4;//MemorySize
	p0[7] = 0;//Terminat
	//printf("22222");
	p0[6] = 0;//RunState
	p0[6]=1;
	while(p0[6]);
	// p0[8] = 0; 

 //  a = bubblesort(number_array,m , n);
   printf("------Sorted Array-------\n");
   for(i=0; i<n; i++)
   {
    printf("%d \n", number_array[i]);
   }
   p0[8] = 0; 
   
   return 0;
}
