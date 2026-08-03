In this example, the aggregation algorithm will create a port of size
104 bits for ports a, and c as the compact=byte option was specified
in the aggregate pragma but the compact=bit default option is used for
port b and its packed size will be 97 bits. The nested structures S
and T are aggregated to encompass three 32 bit member variables (p, m,
and n) and one bit/byte member variable (o).

Note that this example uses the default flow target setting of Vivado
IP to illustrate the aggregation be