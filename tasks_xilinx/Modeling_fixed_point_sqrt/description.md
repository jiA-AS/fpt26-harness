Example code for template function that implements a fixed point square-
root algorithm for HLS.

While the <math.h> (or <cmath>) square-root (sqrt(), sqrtf(), etc) are
supported for HLS, they are always implemented as floating point operations
and result in the instantiation of a CoreGen Floating Point Operator core
in the final RTL, regardless of the types passed.  This template function
can result in a more efficient implementation for fixed point (and integer)
data types while maintaining pr