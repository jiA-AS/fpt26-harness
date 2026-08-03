void TopModule(int    tmax,
               int    nx,
               int    ny,
               double ex[200][240],
               double ey[200][240],
               double hz[200][240],
               double _fict_[100],
               bool   &valid) {

    for (int t = 0; t < tmax; t++) {
        // Top boundary for ey
        for (int j = 0; j < ny; j++) {
            ey[0][j] = _fict_[t];
        }
        // ey interior update
        for (int i = 1; i < nx; i++) {
            for (int j = 0; j < ny; j++) {
                ey[i][j] -= 0.5 * (hz[i][j] - hz[i-1][j]);
            }
        }
        // ex update
        for (int i = 0; i < nx; i++) {
            for (int j = 1; j < ny; j++) {
                ex[i][j] -= 0.5 * (hz[i][j] - hz[i][j-1]);
            }
        }
        // hz update
        for (int i = 0; i < nx-1; i++) {
            for (int j = 0; j < ny-1; j++) {
                hz[i][j] -= 0.7 * (
                    ex[i][j+1] - ex[i][j]
                  + ey[i+1][j] - ey[i][j]
                );
            }
        }
    }

    valid = true;
}
