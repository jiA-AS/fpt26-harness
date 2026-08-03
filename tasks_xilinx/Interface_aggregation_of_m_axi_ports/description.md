In this simple example, the size of the m_axi interface port "arr" is 3 bytes (or 24 bits) but due to the 
specification of the aggregate pragma, the size of the port will be aligned to 4 bytes (or 32 bits) as this 
is the closest power of 2. 

Files Included in this Package
==============================
README  
example.cpp  
example.h  
example_test.cpp  
run_hls.tcl

Running the Design (edit run_hls.tcl to set $hls_exec and enable specific run steps)
=========================================