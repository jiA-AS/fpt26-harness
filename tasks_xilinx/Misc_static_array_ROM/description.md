This example shows how static arrays are mapped to ROMs with different implementations 
and how they are initialized.


Included in this Package
==============================
test.h
test.cpp
test_tb.cpp
run_hls.tcl
README

Running the Design (edit run_hls.tcl to set $hls_exec and enable specific run steps)
=========================================================
vitis-run --mode hls --tcl run_hls.tcl

Things to note:
----------------
[A] In solution_A, you can see that for both BRAM/LUTRAM, th