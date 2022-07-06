; R2 contains the number of which to be converted.
BRzp #4
LD r0, const45
OUT
NOT r2, r2
ADD r2, r2, x1
AND r0, r0, x0
ADD r0, r0, x1
AND r1, r2, r0
BRnp #2
ADD 