This example uses the same design as using_pipos and using_fifos designs to illustrate how the
same design can be converted to use stream of blocks (SOB) as the channel type.

Files Included in this Package
==============================
diamond.cpp  
diamond.h  
diamond_test.cpp  
result.golden.dat  
run_hls.tcl
README

Running the Design (edit run_hls.tcl to set $hls_exec and enable specific run steps)
=========================================================
vitis-run --mode hls --tcl run_hls