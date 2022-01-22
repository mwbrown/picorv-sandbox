
import cocotb
from cocotb.triggers import Timer, FallingEdge
from cocotb.clock import Clock

import itertools

from vhparser import load_le_vh

CLOCK_PERIOD_NS = 1000
RESET_CLOCK_CYCLES = 3

def is_end_condition(dut):

    return dut.rst.value == 0 and \
           dut.rv_mem_valid.value == 1 and \
           dut.rv_mem_addr.value == 0xF00F0000 and \
           dut.rv_mem_byte_wr_ena != 0 and \
           dut.rv_mem_wdata.value == 0xDEADDEAD

def dump_ram(dut):
    for x in range(10):
        print(hex(dut.ram.ram_data[x].value))

@cocotb.test()
async def run_until_fw_end(dut):
   
    #init_rom(dut)
    for (offset, word) in load_le_vh('../fw/output.vh'):
        dut.rom.rom_data[offset >> 2].value = word

    # Run 1MHz clock
    clock = Clock(dut.clk, CLOCK_PERIOD_NS, units='ns')
    cocotb.start_soon(clock.start())

    # Initial reset pulse
    dut.rst.value = 1
    for x in range(RESET_CLOCK_CYCLES):
        await FallingEdge(dut.clk)

    # Release the reset halfway through the low clock
    await Timer(CLOCK_PERIOD_NS / 4, units='ns')
    dut.rst.value = 0

    # Run for 80 clock cycles
    for i in itertools.count():
        await FallingEdge(dut.clk)

        # Look for the magic write at the end of the FW test case.
        try:
            if is_end_condition(dut):
                print('Magic write found!')
                break
        except ValueError: # Happens if a signal is invalid
            print('Error encountered... clocking for trap')
            # Clock for five more clock cycles just in case trap hasn't asserted
            for x in range(15):
                await FallingEdge(dut.clk)
            raise

        if i > 1000000:
            raise IndexError('Test did not complete in time.')

    dump_ram(dut)
