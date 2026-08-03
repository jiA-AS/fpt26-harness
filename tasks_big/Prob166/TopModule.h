#ifndef TOPMODULE_H
#define TOPMODULE_H

#include "ap_int.h"

void TopModule( const BYTE  message[64], ap_uint<32> length, WORD     digest_out[5], bool    &valid );

#endif
