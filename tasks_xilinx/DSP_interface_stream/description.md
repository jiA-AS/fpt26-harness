Description
===========
   C++ source code example for AMD/Xilinx LogiCORE FFT.
   This example is a 1,024 point FFT with stream input and output data.

Files
=====
data         : Directory with data (stimuli and results) used by the testbench.
fft_tb.cpp   : C testbench.
fft_top.cpp  : Top function fft_top.
fft_top.h    : Header file that sets the FFT parameters via its config struct.
run.py       : Script to run C simulation, C synthesis and co-simulation using Vitis.
run_hls.tcl  : Script to 