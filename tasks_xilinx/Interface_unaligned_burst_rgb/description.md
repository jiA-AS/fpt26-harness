This is a simple example using HLS's hls::burst_maxi manual burst (2026.1
unaligned-path extension) to move a non-power-of-2 24-bit struct (rgb_t)
through a 512-bit M-AXI port.

The design batches accesses in groups of 16 rgb_t elements (packed via
hls::vector<rgb_t, 16> into a 384-bit access) and handles the remaining
elements one at a time via the tail (narrow) path. Both the wide-batch
and narrow-tail requests use read_request_unaligned / write_request_unaligned,
so no compile-time alignment 