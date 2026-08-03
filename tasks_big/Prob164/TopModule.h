#ifndef TOPMODULE_H
#define TOPMODULE_H

#include "ap_int.h"

void TopModule(float32_t Qr_i[MAX_ROW*MAX_COL], float32_t Qi_i[MAX_ROW*MAX_COL], int col, int row, float32_t br_i[MAX_ROW], float32_t bi_i[MAX_ROW], float32_t xr_o[MAX_COL], float32_t xi_o[MAX_COL]);

#endif
