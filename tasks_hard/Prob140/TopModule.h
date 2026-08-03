#ifndef TOPMODULE_H
#define TOPMODULE_H

#include "ap_int.h"

void TopModule(ap_uint<1> in, ap_uint<1> reset, ap_uint<8> &out_byte, ap_uint<1> &done);

#endif
