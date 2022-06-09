save1	.FILL x0
save2	.FILL x0
save3	.FILL x0
STACK_BASE .BLKW 60
STACK_OFFSET .FILL x0
push:			; void pushChar(char r0)
	st r1, save1
	st r2, save2
	ld r2, workingStringLoc
	ld r1, stringOffset
	add r2, r1, r2
	str r0, r2, x0
	add r1, r1, x1
	st r1, stringOffset
	ld r1, save1
	ld r2, save2
	ret
pop:			; char r0 popChar()
	st r1, save1
	st r2, save2
	st r3, save3
	and r3, r3, x0
	ld r2, workingStringLoc
	ld r1, stringOffset
	add r1, r1, #-1
	add r2, r1, r2
	ldr r0, r2, x0
	str r3, r2, x0
	st r1, stringOffset
	ld r1, save1
	ld r2, save2
	ld r3, save3
	ret
