
from amaranth import *

from .soc.cpu import PicoRV32
from .soc.bus import NativeBus, FakePeriph
from .periph.mem import NativeRAM, NativeROM

class PicoSB(Elaboratable):

    def __init__(self) -> None:
        super().__init__()

    def elaborate(self, platform):
        del platform # Unused

        m = Module()

        cpu = PicoRV32()
        m.submodules.cpu = cpu

        ram = NativeRAM(size=1024)
        m.submodules.ram = ram

        rom = NativeROM(size=1024)
        m.submodules.rom = rom

        per = FakePeriph()
        m.submodules.per = per

        bus = NativeBus(page_width=16)
        bus.attach_master(cpu)
        bus.attach_slave(rom, page=0x1000)
        bus.attach_slave(ram, page=0x2000)
        bus.attach_slave(per, page=0x4000)

        m.submodules.bus = bus

        return m
