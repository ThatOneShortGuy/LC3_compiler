.ORIG x3000
	JSR #3
constn10	.FILL #-10
const45	.FILL #45
s	.BLKW #1
	LD r0, constn10
	ST r0, s
	LD r2, s
	BRzp #4
	LD r0, const45
	OUT
	NOT r2, r2
	ADD r2, r2, x1
	AND r0, r0, x0
	ADD r0, r0, x1

	HALT
.END