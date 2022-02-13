
.extern __libc_init_array

.section .reset, "ax", @progbits
.global _start
_start:
    # Not enabling global pointer just yet
	#la gp, __global_pointer$
	la sp, __stack_top
	call _init_regs
	call __libc_init_array
	call main
loop:
	j loop

.section .irq, "ax", @progbits
_irq:
	ebreak

.section .text, "ax", @progbits
_init_regs:
 	ret
