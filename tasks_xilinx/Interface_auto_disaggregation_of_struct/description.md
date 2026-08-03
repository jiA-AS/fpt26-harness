Using a hls::stream object inside a structure that is used in the
interface will cause the struct port to be automatically disaggregated
by the Vitis HLS compiler. The generated RTL interface will contain
separate RTL ports for the hls::stream object s_in (named d_s_in_*)
and separate RTL ports for the array arr (named d_arr_*).


Files Included in this Package
==============================
README  
example.cpp  
example.h  
example_test.cpp  
run_hls.tcl

Running the Design (edit run_hls.tcl t