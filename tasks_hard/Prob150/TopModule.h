#ifndef TOPMODULE_H
#define TOPMODULE_H

#include "ap_int.h"

void TopModule( bool reset, bool data, ap_uint<4> &count, bool &counting, bool &done, bool ack );

#endif
