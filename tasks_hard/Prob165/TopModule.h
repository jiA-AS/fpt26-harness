#ifndef TOPMODULE_H
#define TOPMODULE_H

#include "ap_int.h"

void TopModule(ap_uint<8> in[HEIGHT][WIDTH], ap_uint<8> out1[HEIGHT/2][WIDTH/2], ap_uint<8> out2[HEIGHT/4][WIDTH/4], ap_uint<8> out3[HEIGHT/8][WIDTH/8], ap_uint<8> out4[HEIGHT/16][WIDTH/16]);

#endif
