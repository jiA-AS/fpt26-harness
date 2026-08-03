#ifndef TOPMODULE_H
#define TOPMODULE_H

#include "ap_int.h"

void TopModule( ap_fixed<8,1>    x, const ap_fixed<8,1> h[4], ap_fixed<28,7>   &y, bool        &valid );

#endif
