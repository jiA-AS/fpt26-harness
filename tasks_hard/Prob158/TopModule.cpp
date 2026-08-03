#include <cmath>

void TopModule(const float in[4][4], float out[4][4]) {

    float aug[4][8];

    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            aug[i][j]     = in[i][j];
            aug[i][j + 4] = (i == j) ? 1.0f : 0.0f;
        }
    }

    // Gauss–Jordan elimination with partial pivoting
    for (int i = 0; i < 4; ++i) {
        int pivot = i;
        float maxv = fabsf(aug[i][i]);
        for (int r = i + 1; r < 4; ++r) {
            float v = fabsf(aug[r][i]);
            if (v > maxv) {
                maxv = v;
                pivot = r;
            }
        }
        if (pivot != i) {
            for (int c = 0; c < 8; ++c) {
                float tmp = aug[i][c];
                aug[i][c] = aug[pivot][c];
                aug[pivot][c] = tmp;
            }
        }
        float diag = aug[i][i];
        for (int c = 0; c < 8; ++c) {
            aug[i][c] /= diag;
        }
        for (int r = 0; r < 4; ++r) {
            if (r == i) continue;
            float factor = aug[r][i];
            for (int c = 0; c < 8; ++c) {
                aug[r][c] -= factor * aug[i][c];
            }
        }
    }

    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            out[i][j] = aug[i][j + 4];
        }
    }
}
