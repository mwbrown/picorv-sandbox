
from amaranth import *

from ..soc.peripheral import *

class BasicGpio(MemoryMappedPeripheral):

    def __init__(self) -> None:
        super().__init__()

        # Register definitions.
        self.add_reg('dir', 0x0000, ReadWrite())
        self.add_reg('pin', 0x0004, ReadOnly()),
        self.add_reg('pout', 0x0008, WriteOnly()),

        # These should be attached via comb to tristate IOs at top-level
        self.pins_i = Signal(32)
        self.pins_o = Signal(32)
        self.pins_oe = Signal(32)

        self.sync_ffs = 1
        self.pins_i_sync = [self.pins_i] # Will hold a synchronizer

        self.ports = [
            self.pins_i,
            self.pins_o,
            self.pins_oe
        ]

    def elaborate(self, platform):
        m = super().elaborate(platform)

        # TODO: the dir register would be a prime candidate for
        #       a Storage type register in peripheral.py

        # TODO: plumb out bus errors for misaligned / partial writes on registers

        m.d.comb += self.regs['dir'].data_o.eq(self.pins_oe)

        # dir reg write handling
        with m.If(self.regs['dir'].sel & self.mem_byte_wr_ena_i.any()):
            m.d.sync += self.pins_oe.eq(self.mem_wdata_i)

        # pout reg write handling
        with m.If(self.regs['pout'].sel & self.mem_byte_wr_ena_i.any()):
            m.d.sync += self.pins_o.eq(self.mem_wdata_i)

        # Create synchronizer chain for pin reg
        for i in range(self.sync_ffs):
            self.pins_i_sync.append(Signal(32, name='pins_i_sync{}'.format(i)))
            m.d.sync += self.pins_i_sync[i+1].eq(self.pins_i_sync[i])

        # Assign output data for pin reg to end of sync chain. We use the sync
        # domain here so that even if we have sync_ffs=0, we still latch this on
        # every clock cycle (this is not safe, sync_ffs should always be at least 1)
        m.d.sync += self.regs['pin'].data_o.eq(self.pins_i_sync[-1])

        return m
