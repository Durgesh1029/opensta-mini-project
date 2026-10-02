# 1. Create a clock named 'clk' on the clk port with a period of 1.0 ns
create_clock -name clk -period 1.0 [get_ports clk]

# 2. Set typical constraints for input and output boundaries
set_input_delay 0.1 -clock clk [get_ports data_in]
set_output_delay 0.1 -clock clk [get_ports data_out]
