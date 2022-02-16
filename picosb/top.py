
from amaranth import *

from .soc.cpu import PicoRV32
from .soc.bus import NativeBus, FakePeriph
from .periph.mem import NativeRAM, NativeROM, read_init_bin
from .periph.gpio import BasicGpio

class PicoSB(Elaboratable):

    def __init__(self, firmware=None) -> None:
        super().__init__()

        self.gpio_oe = Signal(32)
        self.gpio_i = Signal(32)
        self.gpio_o = Signal(32)

        self.ports = [
            self.gpio_i,
            self.gpio_o,
            self.gpio_oe,
        ]

        self.firmware=firmware
        self.fw_init=None

    def elaborate(self, platform):
        del platform # Unused

        # Process any ROM initialization files passed in.
        if self.firmware is not None:
            self.fw_init = read_init_bin(self.firmware)

        m = Module()

        cpu = PicoRV32()
        m.submodules.cpu = cpu

        ram = NativeRAM(size=1024)
        m.submodules.ram = ram

        rom = NativeROM(size=1024, init=self.fw_init)
        m.submodules.rom = rom

        gpio = BasicGpio()
        m.submodules.gpio = gpio

        bus = NativeBus(page_width=16)
        bus.attach_master(cpu)
        bus.attach_slave(rom, page=0x1000)
        bus.attach_slave(ram, page=0x2000)

        bus.attach_slave(gpio, page=0x4001)

        m.submodules.bus = bus

        m.d.comb += [
            self.gpio_oe.eq(gpio.pins_oe),
            self.gpio_o.eq(gpio.pins_o),
            gpio.pins_i.eq(self.gpio_i)
        ]

        return m
