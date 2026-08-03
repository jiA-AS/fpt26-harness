This is a simple example using HLS's hls::array_partition library
(hls::gather) to guarantee II=1 parallel access to a cyclically partitioned
array, even when the access indices are only known at runtime.

The design sums 4 strided elements of an array, A[i], A[i+s], A[i+2s],
A[i+3s], where the stride s is a runtime argument. Because s is not known
at compile time, #pragma HLS ARRAY_PARTITION alone cannot prove the 4
parallel accesses land in different banks and would fall back to
sequential (II