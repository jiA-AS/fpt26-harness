#ifndef TOPMODULE_H
#define TOPMODULE_H

#include "ap_int.h"

void TopModule(ap_fixed<8,1> sample_in, const ap_fixed<8,1> coeffs[4], ap_fixed<19,4> &sample_out);

#endif
