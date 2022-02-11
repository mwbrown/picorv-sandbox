
from amaranth import *

from .bus import NativeBusSlave

import re

class _MMReg(Elaboratable):

    def __init__(self):
        self._data_o = Signal(32, name='data_o')
        self._sel = Signal(name='sel')
        self._ready = Signal() # TODO

        # Controls whether the owning MemoryMappedPeripheral will handle
        # generating the mem_ready_o signal for this register.
        self.auto_ack = True

    def elaborate(self, platform):
        # Do nothing with the signals.
        del platform
        return Module()

class ReadWrite(_MMReg):

    def __init__(self):
        super().__init__()

        self.data_o = self._data_o
        self.sel = self._sel

        self.ports = [
            self.data_o,
            self.sel,
        ]

    def elaborate(self, platform):
        return super().elaborate(platform)

class ReadOnly(_MMReg):

    def __init__(self):
        super().__init__()

        self.data_o = self._data_o
        self.sel = self._sel

        self.ports = [
            self.data_o,
            self.sel,
        ]

    def elaborate(self, platform):
        m = super().elaborate(platform)
        return m

class WriteOnly(_MMReg):

    def __init__(self):
        super().__init__()

        self.sel = self._sel

        self.ports = [
            self.sel,
        ]

    def elaborate(self, platform):
        m = super().elaborate(platform)
        m.d.comb += self._data_o.eq(0)
        return m

class MemoryMappedPeripheral(NativeBusSlave):

    def __init__(self) -> None:
        super().__init__()
        self.regs = {} # Convenient access by register name
        self._regs = []

    def _validate_reg_name(self, reg_name : str) -> None:
        if not re.match(r'[a-z_]+', reg_name):
            raise ValueError('Register name "{}" is not a valid identifier.'.format(reg_name))

    def add_reg(self, reg_name, offset, reg):
        self._validate_reg_name(reg_name)
        reg_tuple = (reg_name, offset, reg)
        self.regs[reg_name] = reg
        self._regs.append(reg_tuple)

    def elaborate(self, platform):
        m = super().elaborate(platform)

        if self.regs is None:
            raise RuntimeError('MemoryMappedPeripheral has no defined registers.')

        # Default to not acknowledging a transaction.
        m.d.comb += self.mem_ready_o.eq(0)

        for (name, offset, reg) in self._regs:
            # Create the address decoding logic from the NativeBusSlave signals,
            # and add the register as a submodule to be used by the derived classes.

            self._validate_reg_name(name)

            addr_sel = Signal(name='reg_{}_sel'.format(name))
            m.d.comb += [
                addr_sel.eq(self.mem_valid_i & (self.mem_addr_i == C(offset, 32))),
                reg._sel.eq(addr_sel),
            ]

            # FIXME: the mem_ready_o stays high even after mem_valid_i goes low...
            with m.If(addr_sel):

                # This might (?) not create a mux. Need to verify.
                m.d.comb += [
                    self.mem_rdata_o.eq(reg._data_o),
                ]

                # Generate an ack signal if the register is not handling it.
                m.d.comb += self.mem_ready_o.eq(1 if reg.auto_ack else reg._ready)

            submod_name = 'reg_{}'.format(name)
            m.submodules[submod_name] = reg

        return m


