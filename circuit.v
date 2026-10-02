module simple_circuit (
    input wire clk,
    input wire data_in,
    output wire data_out
);

    wire n1, n2;

    // Launch Register
    dff reg_launch ( .clk(clk), .d(data_in), .q(n1) );

    // Combinational Path (2 Buffers = 0.5ns + 0.5ns = 1.0ns delay)
    buf buffer1 ( .a(n1), .x(n2) );
    buf buffer2 ( .a(n2), .x(data_out) );

    // (In a complete design, data_out would route into a Capture Register)

endmodule

