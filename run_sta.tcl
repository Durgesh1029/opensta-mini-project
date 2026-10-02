# Read the timing behavior library
read_liberty sky130_mock.lib

# Read the circuit structure 
read_verilog circuit.v

# Link everything to the top module
link_design simple_circuit

# Read constraints
read_sdc constraints.sdc

# Generate comprehensive setup timing check reports to stdout
report_checks -path_delay max

# Save report to text file
report_checks -path_delay max > sta_report.txt

# Run Python script to generate visual HTML dashboard
catch { exec python3 generate_html_report.py }
catch { exec python generate_html_report.py }

# Exit the program
exit
