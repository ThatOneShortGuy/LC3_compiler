push:			; void pushChar(char r0)
	st r1, saveStackMem1
	st r2, saveStackMem2
	lea r2, STACK_BASE
	ld r1, STACK_OFFSET
	add r2, r1, r2
	str r0, r2, x0
	add r1, r1, x1
	st r1, STACK_OFFSET
	ld r1, saveStackMem1
	ld r2, saveStackMem2
	ret
pop:			; char r0 popChar()
	st r1, saveStackMem1
	st r2, saveStackMem2
	st r3, saveStackMem3
	and r3, r3, x0
	lea r2, STACK_BASE
	ld r1, STACK_OFFSET
	add r1, r1, #-1
	add r2, r1, r2
	ldr r0, r2, x0
	str r3, r2, x0
	st r1, STACK_OFFSET
	ld r1, saveStackMem1
	ld r2, saveStackMem2
	ld r3, saveStackMem3
	ret
saveStackMem1	.FILL x0
saveStackMem2	.FILL x0
saveStackMem3	.FILL x0
STACK_OFFSET    .FILL x0
STACK_BASE      .FILL x0