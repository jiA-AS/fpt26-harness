#include "ap_fixed.h"

void TopModule(ap_fixed<8,1>  sample_in,
               const ap_fixed<8,1> coeffs[4],
               ap_fixed<19,4> &sample_out) {

    static ap_fixed<19,4> regs[4] = {0, 0, 0, 0};

    ap_fixed<19,4> r0 = regs[0], r1 = regs[1], r2 = regs[2];
    regs[3] = sample_in * coeffs[0] + r2;
    regs[2] = sample_in * coeffs[1] + r1;
    regs[1] = sample_in * coeffs[2] + r0;
    regs[0] = sample_in * coeffs[3];

    sample_out = regs[3];
}
