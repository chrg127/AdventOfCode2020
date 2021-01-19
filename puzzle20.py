import sys
import functools
import queue
import math

class Link:
    def __init__(self, num, myside, otherside):
        self.num = num
        self.myside = myside
        self.otherside = otherside
    def __repr__(self):
        return "(" + str(self.num) + ", " + str(self.myside) + ", " + str(self.otherside) + ")"

SIDE_NONE   = -1
SIDE_UP     = 0
SIDE_RIGHT  = 1
SIDE_DOWN   = 2
SIDE_LEFT   = 3
SIDE_UP_M   = 4
SIDE_RIGHT_M= 5
SIDE_DOWN_M = 6
SIDE_LEFT_M = 7

def check_side(p, q, arange, brange):
    for i, j in zip(arange, brange):
        if p[i] != q[j]: return False
    return True

# check two patterns, see if they match
def match(p, q):
    sides = [range(0, 10, 1),   range(9, 100, 10), range(90, 100, 1), range(0, 91, 10),      # up, right, down, left
             range(9, -1, -1),  range(99, 8, -10), range(99, 89, -1), range(90, -1, -10)]    # up-m, down-m, right-m, left-m
    for i in range(0, len(sides)):
        for j in range(0, len(sides)):
            if check_side(p, q, sides[i], sides[j]): return (True, i, j)
    return False, -1, -1

def search(arr, num):
    for link in arr:
        if link.num == num: return link
    return Link(-1, -1, -1)

def make_tab(nums, patterns):
    # tab[p] = [ (number, side of tile p, side of other tile), ...]
    link_tab = {}
    for n in nums: link_tab[n] = []
    for i in range(0, len(nums)):
        for j in range(0, len(nums)):
            if i == j: continue
            a = nums[i]
            b = nums[j]
            link_qp = search(link_tab[b], a) # check if there's already a link from p to q, by searching q's links
            if link_qp.num != -1:
                link_tab[a].append(Link(b, link_qp.otherside, link_qp.myside))
                continue
            if j <= i: continue # skip some checks even if no link is found
            matches, side_a, side_b = match(patterns[i], patterns[j]) # check if the two patterns match some side
            if not matches:
                continue
            link_tab[a].append(Link(b, side_a, side_b))
    return link_tab

# copy pattern from src to dest, starting at the position bufpos in src
# src is copied the natural way, but with some trickery i copy dest in
# some weird orientation according to sides
def copy_pattern(dest, src, sides, bufpos, line_len):
    if bufpos[0] < 0 or bufpos[1] < 0:
        print("copy_pattern: error: passed a negative value")
        sys.exit(1)
    ranges = [range(0, 10, 1), range(9, -1, -1)]
    # for i, y in zip(range(9, -1, -1), range(0, 10, 1)):
    #   for j, x in zip(range(9, -1, -1), range(0, 10, 1)):
    #       src_pos = y*10 + x
    #       dest_pos = (-10 + i) * 120 + (120 + j)
    #       dest[dest_pos] = src[src_pos]
    for i, y in zip(ranges[sides[1]], ranges[0]):
        for j, x in zip(ranges[sides[0]], ranges[0]):
            src_pos = y*10 + x
            dest_pos = (bufpos[1] + i) * line_len + (bufpos[0] + j)
            # print("dest_pos: " + str(dest_pos))
            try:
                dest[dest_pos] = src[src_pos]
            except:
                print("copy_pattern(" + str(sides) + ", " + str(bufpos) + ", " + str(line_len))
                sys.exit(1)

def print_pattern(buf, npertile, ntl, orientation):
    l = npertile * ntl
    ranges = [range(0, l, 1), range(l-1, -1, -1), range(0, l, 1), range(l-1, -1, -1)]
              #range(0, l, 1), range(l-1, -1, -1), range(0, l, 1), range(l-1, -1, -1)]
    xr, yr = 0, 2
    xr += (orientation & 4) >> 2
    yr += (orientation & 2) >> 1
    if bool(orientation & 1): xr, yr = yr, xr
    for y in ranges[yr]:
        for x in ranges[xr]:
            # if x % npertile == 0: print(" ", end="")
            realx, realy = (x, y) if not (orientation & 1) else (y, x)
            # print(str(realx) + "," + str(realy) + " ", end="")
            print(buf[realy*ntl*npertile + realx], end="")
        print("")
        # if y % npertile == 0: print("")

def part1(nums, tab):
    return functools.reduce(lambda x,y: x*y, filter(lambda n: len(tab[n]) == 2, nums))

def calc_orientation(ss, se, initpos_pair):
    lookup = [0, 2, 3, 1]
    offset = [0, -1, 1, 2]
    initpos = initpos_pair[0] << 1 | initpos_pair[1]
    indx = se - (ss - 4 if ss > 3 else ss)
    tmp = ((ss % 2 == 0)+1) if ss > 3 else 0
    ofs = offset[initpos] + offset[tmp]
    orn = lookup[(indx + ofs)%4]
    return ((orn & 2) >> 1, orn & 1)

# return a function that tells what to do to go from src side to dst side when side_n is the side of the other node
def apply_transform(srcn, dstn, srcm, dstm):
    # print("srcn: " + str(srcn) + "dstn: " + str(dstn) + "srcm: " + str(srcm) + "dstm: " + str(dstm))
    isodd = srcm % 2 == 0
    doflip = srcm >= 4
    def flip_ud(x): return [4, 3, 6, 1, 0, 7, 2, 5][x]
    def flip_lr(x): return [2, 5, 0, 7, 6, 1, 4, 3][x]
    def try_flip(x):
        if   doflip and isodd:     return flip_ud(x)
        elif doflip and not isodd: return flip_lr(x)
        else:                      return x
    def rotate(x, diff): return ((x + diff) % 4) + (4 if x >= 4 else 0)
    if srcn < 4 or srcm < 4:
        tmp_srcn = try_flip(srcn)
    else:
        tmp_srcn = srcn
    pair = (max(tmp_srcn, srcm), min(tmp_srcn, srcm))
    # print(str(pair))
    def transform(x):
        res = try_flip(x)
        newres = rotate(res, dstm - (srcm - 4 if doflip else srcm))
        #return newres
        noflip   = [(2, 1), (3, 0), (4, 0), (5, 1), (6, 2), (7, 3), (6, 5), (7, 4)]
        nochange = [(0, 2), (1, 3), (2, 0), (3, 1), (4, 6), (5, 7), (6, 4), (7, 5)]
        thirdres = 0
        if pair not in noflip and pair not in nochange:
            # print("======== gotta flip!!!!!!! ============")
            if srcn in [0, 2, 4, 6]:
                # print("newres: " + str(newres))
                thirdres = [0, 3, 2, 1, 4, 7, 6, 5][newres] # flip horizontally
            else:
                thirdres = [2, 1, 0, 3, 6, 5, 4, 7][newres] # flip vertically
        else:
            thirdres = newres
        return thirdres
    return transform

# adjust: fix the link between n and m
def adjust(currlink, tab, n, m, side_n, side_m, or_tab):
    # print("adjusting " + str(n) + "->" + str(m) + " change: (" + str(currlink.myside) + "," + str(currlink.otherside) + ")->(" + str(side_n) + "," + str(side_m) + ")")
    f = apply_transform(currlink.myside, side_n, currlink.otherside, side_m)
    # GOD FUCKING DAMMIT
    tmp_side_n = side_n
    # fix n->m and m->n
    currlink.myside = side_n
    link = search(tab[m], n)
    link.otherside = side_n
    or_tab[m] = calc_orientation(link.myside, side_m, or_tab[m])
    # ugh... do we have to do something to this?
    if link.myside == side_m:
        return
    for link in tab[m]:
        newvalue = f(link.myside)
        # print(str(m) + "->" + str(link.num) + ": " + str(link.myside) + "->" + str(newvalue))
        link.myside = newvalue
        otherlink = search(tab[link.num], m)
        # print(str(link.num) + "->" + str(m) + ": " + str(otherlink.otherside) + "->" + str(newvalue))
        otherlink.otherside = newvalue

def find_start_pos(tab, startnode, line_len):
    arr = tab[startnode]
    n1, n2 = arr[0].myside, arr[1].myside
    l = line_len * 10 - 10
    if n1 == 0 or n1 == 2: return ( [0, 0, l, 0][n1], [0, l, 0, 0][n2] )
    else:                  return ( [0, 0, l, 0][n2], [0, l, 0, 0][n1] )

def rebuild_image(nums, patt, tab):
    start_num = next(filter(lambda n: len(tab[n]) == 2, nums))
    buf = ['0'] * (len(nums)*100)
    q = queue.Queue(len(nums))
    visited_nodes, visited_links, orientation_tab = {}, {}, {}
    for n in nums:
        visited_nodes[n] = False
        orientation_tab[n] = (0, 0)
        for m in nums: visited_links[m*n] = False
    tmppos = find_start_pos(tab, start_num, int(math.sqrt(len(nums))))
    q.put( (start_num, tmppos[0], tmppos[1]) )
    visited_nodes[start_num] = True
    while not q.empty():
        n, bposx, bposy = q.get()
        print("copying " + str(n) + " with orientation: " + str(orientation_tab[n]) + " pos: " + str(bposx) + "," + str(bposy) + " index:" + str(nums.index(n)))
        copy_pattern(buf, patt[nums.index(n)], orientation_tab[n], (bposx, bposy), int(math.sqrt(len(nums)) * 10))
        visited_sides = [-1]*4
        for link in tab[n]:
            if not visited_links[n*link.num]:
                #print("visiting link: " + str(n) + "->" + str(link.num))
                visited_links[n*link.num] = True
                mutual_sides = [ 2, 3, 0, 1, 6, 7, 4, 5 ]
                if link.myside > 3: # do we have a mirrored side?
                    # then DONT' DON'T DON'T TRY TO FIX THE FUCKING link.myside OR ELSE I WILL KILL YOU
                    # link.myside WILL BE FUCKING FIXED IN adjust() DON'T TRY TO FIX IT NOW
                    adjust(link, tab, n, link.num, link.myside - 4, mutual_sides[link.myside - 4], orientation_tab)
                elif link.otherside != mutual_sides[link.myside]:
                    adjust(link, tab, n, link.num, link.myside, mutual_sides[link.myside], orientation_tab)
            if not visited_nodes[link.num]:
                # print("deciding pos: bposx=" + str(bposx) + ", bposy:" + str(bposy) + ", myside:" + str(link.myside))
                tmpx = bposx + ([0, 10, 0, -10][link.myside])
                tmpy = bposy + ([-10, 0, 10, 0][link.myside])
                print("inserting " + str(link.num) + ", " + str(bposx) + "," + str(bposy) + " " + str(tmpx) + "," + str(tmpy))
                q.put( (link.num, tmpx, tmpy) )
                visited_nodes[link.num] = True
    return buf

sea_monster = [ "OOOOOOOOOOOOOOOOOO#O",
                "#OOOO##OOOO##OOOO###",
                "O#OO#OO#OO#OO#OO#OOO", ]
smw = 20 #len(sea_monster[0])
smh = 3 #len(sea_monster)
monster_pos = [ (0, 1), (1, 2), (4, 2), (5, 1), (6, 1), (7, 2), (10, 2), (11, 1), (12, 1), (13, 2), (16, 2), (17, 1), (18, 0), (18, 1), (19, 1) ]
def match_seamonster(buf, bufw, stx, sty, orientation):
    def translate(x, y, orientation):
        # if bool(orientation & 1):        x, y = y, x
        # if bool((orientation & 2) >> 1): y = smw - y
        # if bool((orientation & 4) >> 2): x = smw - x
        if not bool(orientation & 1):
            if bool((orientation & 4) >> 2): x = smw - x
            if bool((orientation & 2) >> 1): y = smh - y
        else:
            x, y = y, x
            if bool((orientation & 4) >> 2): x = smh - x
            if bool((orientation & 2) >> 1): y = smw - y
        return (stx + x, sty + y)
    for mx, my in monster_pos:
        bufx, bufy = translate(mx, my, orientation)
        bufpos = (bufy * bufw) + bufx
        if buf[bufpos] != '#': return 0
        # print("translate(" + str(stx) + ", " + str(sty) + ", " + str(mx) + ", " + str(my) + ") = " + str(bufx) + ", " + str(bufy))
        # print("didn't match: " + str(stx) + "," + str(sty) + ", " + str(mx) + "," + str(my))
    print("found a match at: " + str(stx) + "," + str(sty) + ", or: " + str(orientation))
    for mx, my in monster_pos:
        bufx, bufy = translate(mx, my, orientation)
        bufpos = bufy * bufw + bufx
        buf[bufpos] = 'O'
    return 1

def find_sea_monsters(buf, length, orientation):
    ranges = [range(0, length-smw, 1), range(length-smw-1, -1, -1), range(0, length-smh, 1), range(length-smh-1, -1, -1)]
    xr, yr = 0, 2
    if bool(orientation & 1): xr, yr = yr, xr
    xr += (orientation & 4) >> 2
    yr += (orientation & 2) >> 1
    res = 0
    for y in ranges[yr]:
        for x in ranges[xr]:
            res += match_seamonster(buf, length, x, y, orientation)
    return res

def count_hashes(buf, length):
    return len(list(filter(lambda x: x == '#', buf)))

def strip_borders(buf, ntl):
    res, i = ['0'] * ntl*ntl*64, 0
    for y in range(0, ntl*10):
        if y % 10 == 0 or y % 10 == 9: continue
        for x in range(0, ntl*10):
            if x % 10 == 0 or x % 10 == 9: continue
            res[i] = buf[y*ntl*10 + x]
            i += 1
    return res

def part2(nums, patt, tab):
    buf = rebuild_image(nums, patt, tab)
    for n in nums: print(str(n) + ": " + str(tab[n]))
    ntl = int(math.sqrt(len(nums)))
    # print_pattern(buf, 10, ntl, 3)
    newbuf = strip_borders(buf, ntl)
    for i in range(0, 8):
        tmpbuf = newbuf.copy()
        nmonsters = find_sea_monsters(tmpbuf, ntl*8, i)
        nhashes = count_hashes(tmpbuf, ntl*8)
        print("sea monsters found: " + str(nmonsters) + ", number of #: " + str(nhashes))

filename = "aaa.txt"
# filename = "input20.txt"
lines = list(filter(lambda x: x != "", [l.strip() for l in open(filename)]))
nums, patterns = [], []
for i in range(0, len(lines), 11):
    nums.append(int(lines[i][5:-1]))
    patt = ""
    for j in range(i+1, i+11):
        patt += lines[j]
    patterns.append(patt)
link_tab = make_tab(nums, patterns)
for n in nums: print(str(n) + ": " + str(link_tab[n]))
part2(nums, patterns, link_tab)
# buf = "OOOOOOOOOOOOOOOOOO#O#OOOO##OOOO##OOOO###O#OO#OO#OO#OO#OO#OOO"
