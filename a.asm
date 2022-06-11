.ORIG x3000
	JSR #10
const3	.FILL #3
const5	.FILL #5
const2	.FILL #2
const6	.FILL #6
num	.BLKW #1
c	.BLKW #1
ch	.BLKW #1
alloc	.BLKW #5
arr	.BLKW #5
s	.BLKW #1
	LD r0, const3
	LD r1, const5
	LD r2, const2
	AND r3, r1, x0
	ADD r3, r3, r1
	ADD r2, r2, #-1
	BRP #-3
	ADD r2, r0, r3
	LD r3, const5
	LD r0, const2
	ADD r1, r3, r0
	LD r0, const5
	LD r3, const6
	AND r4, r0, x0
	ADD r4, r4, r0
	ADD r3, r3, #-1
	BRP #-3
	NOT r4, r4
	ADD r4, r4, x1
	ADD r3, r1, r4
	NOT r3, r3
	ADD r3, r3, x1
	ADD r4, r2, r3
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
.END