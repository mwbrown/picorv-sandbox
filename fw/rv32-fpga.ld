/* Small linker script to give the test RV32 core
 * a small amount of RAM/ROM.
 */

OUTPUT_ARCH(riscv)
ENTRY(_start)

__rom_length = 0x400;
__ram_length = 0x400;

MEMORY
{
    ROM (rx)  : ORIGIN = 0x10000000 LENGTH=__rom_length
    RAM (rwx) : ORIGIN = 0x20000000 LENGTH=__ram_length
}

SECTIONS
{
  .reset 0x10000000:
  {
    . = ALIGN(4);

    KEEP (*(SORT_NONE(.reset)))

    . = ALIGN(4);
  } >ROM

  PROVIDE ( __reset_end = . );

  .irq 0x10000020 :
  {
    . = ALIGN(4);

    KEEP (*(SORT_NONE(.irq)))

    . = ALIGN(4);
  } >ROM

  PROVIDE ( __irq_end = . );

  .text : 
  {
    . = ALIGN(4);

    *(.text)
    *(.text.*)

    . = ALIGN(4);
    _etext = .;
  } >ROM

  PROVIDE ( __text_end = . );

  .rodata :
  {
    . = ALIGN(4);
    *(.rodata)
    *(.rodata*)
    *(.srodata)
    *(.srodata*)
    . = ALIGN(4);
  } >ROM

  _sidata = LOADADDR(.data);

  .data :
  {
    . = ALIGN(4);
    _sdata = .;

    *(.data)
    *(.data*)

    . = ALIGN(4);
    _edata = .;
  } >RAM AT> ROM

  . = ALIGN(4);
  .bss :
  {
    _sbss = .;

    *(.bss)
    *(.bss*)

    . = ALIGN(4);
    _ebss = .;
  } >RAM

  PROVIDE( __stack_top = 0x20000000 + __ram_length );
}
