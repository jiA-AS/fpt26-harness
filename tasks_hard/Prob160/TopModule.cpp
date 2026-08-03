void TopModule(const unsigned char data[256], unsigned int length, unsigned int &crc_out){

    unsigned int crc = 0xFFFFFFFFu;
    // Process each byte
    for (unsigned int i = 0; i < length; ++i) {
        crc ^= data[i];
        // Process 8 bits
        for (int b = 0; b < 8; ++b) {
            if (crc & 1u)
                crc = (crc >> 1) ^ 0xEDB88320u;
            else
                crc =  crc >> 1;
        }
    }
    // Final XOR
    crc_out = ~crc;
}
