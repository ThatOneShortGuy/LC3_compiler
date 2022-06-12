.ORIG x3000
	JSR #20
const1	.FILL #1
const2	.FILL #2
const3	.FILL #3
const4	.FILL #4
const5	.FILL #5
const97	.FILL #97
const6	.FILL #6
alloc	.BLKW #5
arr	.BLKW #5
c	.BLKW #1
num	.BLKW #1
ch	.BLKW #1
	LEA r0, arr
	LD r1, const1
	STR r1, r0, #0
	LD r1, const2
	STR r1, r0, #1
	LD r1, const3
	STR r1, r0, #2
	LD r1, const4
	STR r1, r0, #3
	LD r1, const5
	STR r1, r0, #4
	LD r0, const97
	LD r1, const1
	ADD r2, r0, r1
	ST r2, c
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
	ST r4, num
	LD r0, c
	LD r1, num
	ADD r2, r0, r1
	ST r2, ch

.END