This example shows how to debug a data-driven task-level parallelsim model that deadlocks when
running C simulation.

Files Included in this Package
==============================
test.cpp  
test.h  
test_tb.cpp  
run_hls.tcl
README

Running the Design (edit run_hls.tcl to set $hls_exec and enable specific run steps)
=========================================================
vitis-run --mode hls --tcl run_hls.tcl

Steps to debug the resulting deadlock error that is reported by csim_design command