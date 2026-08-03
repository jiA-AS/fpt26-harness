#include "ap_int.h"

void TopModule(ap_int<32> in[8], ap_int<32> out[8], bool &valid) {

    ap_int<32> a[8];

    for (int i = 0; i < 8; i++) {
        a[i] = in[i];
    }

    for (int i = 0; i < 7; i++) {
        for (int j = i+1; j < 8; j++) {
            if (a[i] > a[j]) {
                ap_int<32> tmp = a[i];
                a[i] = a[j];
                a[j] = tmp;
            }
        }
    }

    for (int i = 0; i < 8; i++) {
        out[i] = a[i];
    }

    valid = true;
}
