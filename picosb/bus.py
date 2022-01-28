
from amaranth import *

class NativeBusMaster(Elaboratable):

    def __init__(self) -> None:
        super().__init__()

        self.mem_valid_o = Signal() # Bus access valid output (asserted until acked).
        self.mem_addr_o = Signal(32) # Bus address output.
        self.mem_instr_o = Signal() # Instruction fetch. Currently ignored.
        self.mem_wdata_o = Signal(32) # Bus data output.
        self.mem_byte_wr_ena_o = Signal(4) # Byte enable.
        self.mem_rdata_i = Signal(32) # Bus data input.
        self.mem_ready_i = Signal() # Bus acknowledge input.

    def elaborate(self, platform):
        del platform # Unused

        m = Module()
        return m

class NativeBusSlave(Elaboratable):

    def __init__(self) -> None:
        super().__init__()

        self.mem_valid_i = Signal() # Bus access valid input (asserted until acked).
        self.mem_addr_i = Signal(32) # Bus address input.
        self.mem_instr_i = Signal() # Instruction fetch. Currently ignored.
        self.mem_wdata_i = Signal(32) # Bus data input.
        self.mem_byte_wr_ena_i = Signal(4) # Byte enable.
        self.mem_rdata_o = Signal(32) # Bus data output.
        self.mem_ready_o = Signal() # Bus acknowledge output.

    def elaborate(self, platform):
        del platform # Unused

        m = Module()
        return m

class NativeBus(Elaboratable):
    def __init__(self, *, page_width) -> None:
        super().__init__()

        self.master = None
        self.slaves = {}
        self.page_width = page_width

    def attach_master(self, m : NativeBusMaster) -> None:
        if self.master is not None:
            raise RuntimeError('Native bus already has attached master.')

        self.master = m

    def attach_slave(self, m : NativeBusSlave, page : int) -> None:
        if page in self.slaves:
            raise KeyError('Page {} already allocated on native bus.'.format(hex(page)))

        self.slaves[page] = m

    def elaborate(self, platform):
        del platform # Unused

        if self.master is None:
            raise RuntimeError('Native bus is missing master.')

        m = Module()

        # Aliases
        mem_valid = self.master.mem_valid_o
        mem_addr = self.master.mem_addr_o
        mem_instr = self.master.mem_instr_o
        mem_wdata = self.master.mem_wdata_o
        mem_byte_wr_ena = self.master.mem_byte_wr_ena_o
        mem_rdata = self.master.mem_rdata_i
        mem_ready = self.master.mem_ready_i

        # Create a sub-signal for the upper address bits, to indicate the page.
        mem_page = mem_addr.bit_select(32 - self.page_width, self.page_width)
        page_shape = Shape(self.page_width)

        for page, s in self.slaves.items():
            addr_valid = mem_valid & mem_page == C(page, page_shape)

            m.d.comb += [
                s.mem_valid_i.eq(addr_valid),
                s.mem_addr_i.eq(mem_addr),
                s.mem_instr_i.eq(mem_instr),
                s.mem_wdata_i.eq(mem_wdata),
                s.mem_byte_wr_ena_i.eq(mem_byte_wr_ena),
            ]

            with m.If(addr_valid):
                m.d.comb += [
                    mem_rdata.eq(s.mem_rdata_o),
                    mem_ready.eq(s.mem_ready_o)
                ]

        # TODO attach master
        return m

class FakePeriph(NativeBusSlave):

    def __init__(self) -> None:
        super().__init__()

    def elaborate(self, platform):
        m = super().elaborate(platform)

        # Just generate an ack every time this thing goes valid.
        m.d.comb += self.mem_ready_o.eq(1)

        return m
