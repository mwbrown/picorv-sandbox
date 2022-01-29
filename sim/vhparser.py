
# RISC-V images for this system start at 0x10000000
# TODO: move this somewhere common?
DEFAULT_BASEADDR=0x10000000
DEFAULT_MAXLEN=256*4

def rev32(i):
    b = i.to_bytes(4, byteorder='little')
    return int.from_bytes(b, byteorder='big', signed=False)

def load_le_vh(filename):

    offset = 0

    # objcopy produces files with CRLF line terminators
    with open(filename, 'r') as f:
        for line in map(str.strip, f.readlines()):

            if line.startswith('@'):
                addr = int(line[1:], base=16)
                print('ORG {}'.format(hex(addr)))
                # Parse address (big-endian)
                offset = addr - DEFAULT_BASEADDR
                continue

            # Read the 32-bit words (little-endian, needs conversion)
            for word in line.split():
                le_word = int(word, base=16)
                be_word = rev32(le_word)

                # Sanity check the offset.
                if offset < 0 or offset >= DEFAULT_MAXLEN:
                    raise IndexError('Program exceeds boundary (off={}).'.format(offset))

                # This tuple can be given straight to the rom as
                # dut.rom.rom_data[offset].value = be_word
                yield (offset, be_word)
                offset += 4
