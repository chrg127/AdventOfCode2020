import sys
import functools

def check_side(p, q, arange, brange):
    for i, j in zip(arange, brange):
        if p[i] != q[j]: return False
    return True

SIDE_NONE   =  0
SIDE_LEFT   =  1
SIDE_RIGHT  = -1
SIDE_UP     =  2
SIDE_DOWN   = -2

# check two patterns, see if they match
def check(p, q):
    sides = [range(0, 10, 1),   range(90, 100, 1), range(9, -1, -1),  range(99, 89, -1),     # up, down, up mirrored, down mirrored
             range(9, 100, 10), range(0, 91, 10),  range(99, 8, -10), range(90, -1, -10)]    # left, right, left mirrored, right mirrored
    for sidep in sides:
        for sideq in sides:
            if check_side(p, q, sidep, sideq): return (True, SIDE_UP)
    # for side in [
    #         (horz[0], horz[0], SIDE_UP),    (horz[0], horz[1], SIDE_UP),    (horz[0], horz[2], SIDE_UP),    (horz[0], horz[3], SIDE_UP),
    #         (horz[1], horz[0], SIDE_DOWN),  (horz[1], horz[1], SIDE_DOWN),  (horz[1], horz[2], SIDE_DOWN),  (horz[0], horz[3], SIDE_DOWN),
    #         (vert[0], vert[0], SIDE_LEFT),  (vert[0], vert[1], SIDE_LEFT),  (vert[0], vert[2], SIDE_LEFT),  (vert[0], vert[3], SIDE_LEFT),  
    #         (vert[1], vert[0], SIDE_RIGHT), (vert[1], vert[1], SIDE_RIGHT), (vert[1], vert[2], SIDE_RIGHT), (vert[0], vert[3], SIDE_RIGHT)
    #         ]:
    #     if check_side(p, q, side[0], side[1]): return (True, side[2])
    return False, 0

def search(arr, num):
    for elem in arr:
        if elem[0] == num: return elem
    return (-1, 0)

lines = list(filter(lambda x: x != "", [l.strip() for l in open("input20.txt")]))
nums = []
patterns = []
for i in range(0, len(lines), 11):
    nums.append(int(lines[i][5:-1]))
    pattern = ""
    for j in range(i+1, i+11):
        pattern += lines[j]
    patterns.append(pattern)

# tab[number] = [ (number, side), (number, side), ...]
link_tab = {}
for n in nums: link_tab[n] = []

for i in range(0, len(nums)):
    for j in range(0, len(nums)):
        if i == j: continue
        a = nums[i]
        b = nums[j]
        found, side = search(link_tab[b], a) # check if there's already a link from p to q, by searching q's links
        if found != -1:
            link_tab[a].append((b, -side))
            continue
        if j <= i: continue # skip some checks even if no link is found
        matches, side = check(patterns[i], patterns[j]) # check if the two patterns match some side
        if not matches:
            continue
        link_tab[a].append((b, side))

prod = functools.reduce(lambda x,y: x*y, filter(lambda n: len(link_tab[n]) == 2, nums))
print(prod)
