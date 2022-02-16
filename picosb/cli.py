#!/usr/bin/env python3

import argparse
from sys import stdout

from amaranth.back import verilog
from .top import PicoSB

def get_parser():
    p = argparse.ArgumentParser()
    p.add_argument('-o', '--output', help='Writes verilog to OUTPUT', required=True)
    p.add_argument('--firmware', help='Initializes ROM with a particular binary file.')
    return p

# Run the Amaranth verilog backend. This will instantiate the "top level" module to generate
# exported RTL without necessarily building against any of the actual HW platforms.
#
# To build for a real FPGA, use a module in picosb.platforms instead.
#
if __name__ == '__main__':

    parser = get_parser()
    args = parser.parse_args()

    dut = PicoSB(firmware=args.firmware)

    output = verilog.convert(dut, ports=dut.ports)

    if args.output == '-':
        stdout.write(output)
    else:
        with open(args.output, 'w') as f:
            f.write(output)
            f.flush()
