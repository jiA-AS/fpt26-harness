void TopModule(int* in1, int* in2, int* out_r, int size, int rep_count) {

    // Local buffers
    int A[16][16];
    int B[16][16];
    int C[16][16];


    // Read in1 → A
    LOAD_A:
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            A[i][j] = in1[i * size + j];
        }
    }

    // Read in2 → B
    LOAD_B:
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            B[i][j] = in2[i * size + j];
        }
    }

    // Perform rep_count rounds of block‑matrix multiply
    COMPUTE:
    for (int r = 0; r < rep_count; ++r) {
    row_loop:
        for (int row = 0; row < size; ++row) {
        k_loop:
            for (int k = 0; k < size; ++k) {
                int acc = 0;
            col_loop:
                for (int col = 0; col < size; ++col) {
                    acc += A[row][col] * B[col][k];
                }
                C[row][k] = acc;
            }
        }
    }

    // Write C → out_r
    WRITE:
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            out_r[i * size + j] = C[i][j];
        }
    }
}
