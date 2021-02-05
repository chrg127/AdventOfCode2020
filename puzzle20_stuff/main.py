class Link:
    def __init__(self, num, myside, otherside, ox, oy):
        self.num = num
        self.myside = myside
        self.otherside = otherside
        self.ox = ox
        self.oy = oy


# return a function that tells what to do to go from src side to dst side
def apply_transform(src, dst):
    isodd = src % 2 == 0
    isflip = src >= 4
    def flip_ud(x): return [4, 3, 6, 1, 0, 7, 2, 5][x]
    def flip_lr(x): return [2, 5, 0, 7, 6, 1, 4, 3][x]
    def rotate(x, diff): return ((x + diff) % 4) + (4 if x >= 4 else 0)
    def transform(x):
        res = 0
        if   isflip and     isodd: res = flip_ud(x)
        elif isflip and not isodd: res = flip_lr(x)
        else:                      res = x
        return rotate(res, dst - (src - 4 if isflip else src))
    return transform
f = apply_transform(1, 2)
for i in range(0, 8):
    print(str(i) + "->" + str(f(i)))
