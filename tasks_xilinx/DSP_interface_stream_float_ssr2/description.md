Description
===========
       C++ source code example for AMD/Xilinx LogiCORE FFT.
       This example is a 1,024 pts FFT (SSR=2) with floating-point data.
       (the FFT_SSR user macro in fft_top.h can modify this example to create a 64 pts FFT with SSR=4)
 
Files
=====
data-ssr2    : Directory with data (stimuli and results) used by the testbench (SSR=2).
data-ssr4    : Directory with data when macro FFT_SSR is set to 4 (SSR=4).
fft_tb.cpp   : C testbench.
fft_top.cpp  : Top function fft_top