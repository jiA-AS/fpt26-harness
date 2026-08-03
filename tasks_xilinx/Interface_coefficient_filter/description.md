Example code for a scaled-integer fixed-point Hamming window function.
This example is intended to demonstrates the recommended coding style
when an array should be implemented as a ROM.  The key guideline is that
the ROM's source (in the C code) array should be initialized by a sub-
function to the function that access (reads from) the array.  When the
array is properly inferred to be a ROM, the initialization function will
be optimized away during HLS.

Files Included in this Package
=========