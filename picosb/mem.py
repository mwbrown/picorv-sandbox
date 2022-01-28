
from amaranth import *

from .bus import NativeBusSlave

class NativeMemory(NativeBusSlave):
    def __init__(self, *, size, is_ram, is_async=False) -> None:
        super().__init__()

        # TODO probably want to limit this to power-of-two instances
        if (size % 4) != 0:
            raise ValueError('RAM size must be divisible by 4.')

        self.depth = size // 4
        self.is_ram = is_ram
        self.is_async = is_async

    def elaborate(self, platform):
        m = super().elaborate(platform)

        domain = 'comb' if self.is_async else 'sync'

        mem = Memory(width=32, depth=self.depth)

        rp = mem.read_port(transparent=False, domain=domain)
        m.submodules.rd_port = rp

        if self.is_ram:
            # This memory bus is read-or-write, never both.
            # So the read enable is simply if the write enable is all zeroes
            read_en = ~self.mem_byte_wr_ena_i.any()

            # Create a write port additionally for RAMs.
            wp = mem.write_port(granularity=8, domain=domain)
            m.submodules.wr_port = wp

            # Assign the write port to the NativeBusSlave signals.
            m.d.comb += [
                wp.addr.eq(self.mem_addr_i),
                wp.data.eq(self.mem_wdata_i),
                wp.en.eq(self.mem_byte_wr_ena_i),
            ]

        else:
            # This is a ROM.
            read_en = C(1)

        # Assign the read port to the NativeBusSlave signals.
        m.d.comb += [
            rp.en.eq(read_en),
            rp.addr.eq(self.mem_addr_i),
            self.mem_rdata_o.eq(rp.data),
        ]

        if self.is_async:
            # Always assert mem_ready when our address select is active.
            m.d.comb += [
                self.mem_ready_o.eq(self.mem_valid_i)
            ]
        else:
            # Generate a signal to indicate a low-to-high mem_valid edge.
            mem_valid_prev = Signal()

            # Acknowledge the transaction on the next cycle.
            m.d.sync += [
                mem_valid_prev.eq(self.mem_valid_i),
                self.mem_ready_o.eq(~mem_valid_prev & self.mem_valid_i),
            ]

        return m

class NativeRAM(NativeMemory):

    def __init__(self, size=1024) -> None:
        super().__init__(size=size, is_ram=True)

class NativeROM(NativeMemory):

    def __init__(self, *, size=1024) -> None:
        super().__init__(size=size, is_ram=False)
