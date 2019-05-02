# Returns bit y of x (10 base).  i.e.
# bit 2 of 5 is 1
# bit 1 of 5 is 0
# bit 0 of 5 is 1
def getBit(y, x):
    return str((x>>y)&1)

# Returns the first `count` bits of base 10 integer `x`
def tobin(x, count=8):
    shift = range(count-1, -1, -1)
    bits = map(lambda y: getBit(y, x), shift)
    return "".join(bits)

vSize = 128
eSize = [8, 16, 32, 64]
grnl = 8

vector = [511, -1, 0, 3348896]
