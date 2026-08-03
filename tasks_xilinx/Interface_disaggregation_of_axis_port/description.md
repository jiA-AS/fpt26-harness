In this disaggregation example, a struct port is mapped to an AXI
stream and then disaggregated causing the Vitis HLS compiler to create
two AXI stream ports - one for each member (c and i) of the struct A. 

Files Included in this Package
==============================
README  
example.cpp  
example.h  
example_test.cpp  
run_hls.tcl

Running the Design (edit run_hls.tcl to set $hls_exec and enable specific run steps)
=========================================================
vitis-run --mode hl