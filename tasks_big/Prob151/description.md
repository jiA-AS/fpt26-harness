Design a 4-tap symmetric Finite Impulse Response (FIR) filter defined by:
    y[n] = h₀·x[n] + h₁·x[n−1] + h₂·x[n−2] + h₃·x[n−3]

The constant symmetric co-efficients are:
	h = {0.30011, 0.90032, 0.90032, 0.30011}

The circuit should processes one sample per clock cycle and produces a filtered output using a Multiply-Accumulate (MAC) operation on the current and previous three inputs.
Input: sample_in : ap_fixed<8,1> (1 integer + 7 fractional bits, signed)
Output: sample_out : ap_fixed<19,4> (4 integer + 15 fractional bits, signed)

The top-level function should have the following prototype:
void TopModule(ap_fixed<8,1> sample_in, ap_fixed<19,4> &sample_out)