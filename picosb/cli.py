#!/usr/bin/env python3

from amaranth.cli import main
from .top import PicoSB

# Run the Amaranth default CLI. This will instantiate the "top level" module to generate
# exported RTL without necessarily building against any of the actual HW platforms.
#
# To build for a real FPGA, use a module in picosb.platforms instead.
#
if __name__ == '__main__':
    dut = PicoSB()
    main(dut)
