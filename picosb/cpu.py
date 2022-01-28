
from amaranth import *
from .bus import NativeBusMaster

class PicoRV32(NativeBusMaster):

    def __init__(self) -> None:
        super().__init__()

        self.rv_trap = Signal()

    def elaborate(self, platform):
        m = super().elaborate(platform)

        m.submodules += Instance("picorv32",

            i_clk = ClockSignal(),
            i_resetn = ~ResetSignal(),
            o_trap = self.rv_trap,

            # Native memory interface
            o_mem_valid = self.mem_valid_o,
            o_mem_addr = self.mem_addr_o,
            o_mem_wdata = self.mem_wdata_o,
            o_mem_wstrb = self.mem_byte_wr_ena_o,
            o_mem_instr = self.mem_instr_o,
            i_mem_ready = self.mem_ready_i,
            i_mem_rdata = self.mem_rdata_i,

            # Memory lookahead interface (ignored)
            o_mem_la_read = Signal(),
            o_mem_la_write = Signal(),
            o_mem_la_addr = Signal(),
            o_mem_la_wdata = Signal(),
            o_mem_la_wstrb = Signal(),

            # Coprocessor interface (not implemented)
            o_pcpi_valid = Signal(),
            o_pcpi_insn = Signal(32),
            o_pcpi_rs1 = Signal(32),
            o_pcpi_rs2 = Signal(32),
            i_pcpi_wr = C(0), #(1'b0),
            i_pcpi_rd = C(0, Shape(32)), #(32'b0),
            i_pcpi_wait = C(0), #(1'b0),
            i_pcpi_ready = C(0), #(1'b0),

            # IRQ interface (not implemented)
            i_irq = C(0, Shape(32)), #(32'b0),
            o_eoi = Signal(),

            # Trace interface (ignored)
            o_trace_valid = Signal(),
            o_trace_data = Signal(36)
        )

        return m
