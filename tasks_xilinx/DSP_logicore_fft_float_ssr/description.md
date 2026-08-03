Description
===========
       C++ source code example for AMD/Xilinx LogiCORE FFT.
       This example is a 1,024 pts FFT (SSR=2) with floating-point data that supports
       both ARRAY and STREAM interfaces through a compile-time macro.
       
       The USE_STREAM_INTERFACE macro in fft_top.h controls the interface type:
         - Set to 0 for ARRAY interface
         - Set to 1 for STREAM interface (default)
 
Interface Selection
===================
To change the interface type, modify th