
.section .reset, "ax", @progbits
.global _start
_start:
    # Not enabling global pointer just yet
	#la gp, __global_pointer$
	la sp, __stack_top
	la ra, loop
	jal zero, main
loop:
	j loop

.section .irq, "ax", @progbits
_irq:
	ebreak
