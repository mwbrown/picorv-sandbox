
PREFIX=riscv64-unknown-elf-
AS=$(PREFIX)as
CC=$(PREFIX)gcc
LD=$(PREFIX)ld
OBJCOPY=$(PREFIX)objcopy
OBJDUMP=$(PREFIX)objdump

SPECS=-specs=picolibc.specs

CPUFLAGS=-march=rv32ic -mabi=ilp32
ASFLAGS=$(CPUFLAGS)
CFLAGS=$(CPUFLAGS) $(SPECS) -Og -ffunction-sections -fdata-sections
LDFLAGS=$(CPUFLAGS) $(SPECS) -Trv32-fpga.ld -Wl,-Map=output.map -Wl,-gc-sections

.PHONY: all clean

all: output.vh output.lst

clean:
	rm -f src/*.o
	rm -f output.elf output.vh output.lst

output.elf: src/crt0.o src/sim_main.o
	$(CC) $(LDFLAGS) -o $@ -nostartfiles $^

# This seems to generate a file with groups of 4-bytes, in little endian format.
# Since the ROM port is 32-bit, the testbench ROM initializer will need to swap
# the bytes when loading the data into the ROM instance.
%.vh: %.elf
	$(OBJCOPY) -O verilog --verilog-data-width=4 $^ $@

%.lst: %.elf
	$(OBJDUMP) -d $^ > $@
