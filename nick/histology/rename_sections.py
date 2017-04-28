import os, sys
import itertools
import shutil


# Renaming some section images collected in 2 days
# folder = '/home/nick/data/jarahubdata/jarashare/histology/pinp017/orig_p2d2_p3d5'
# start_num = 107

# for indf, f in enumerate(sorted(os.listdir(folder))):
#     newFn = 's-{}.czi'.format(start_num + indf)
#     os.rename(os.path.join(folder, f), os.path.join(folder, newFn))

folder = '/home/nick/data/jarahubdata/jarashare/histology/pinp017/orig_p1d1_p3d5'

nums = range(1, 7)
letters = ['a', 'b', 'c', 'd']
chans = ['tl', 'g', 'r', 'fr']
plates = [1, 2, 3]
extension = '.czi'

start = [1, 'd', 1]
end = [3, 'd', 5]

# print ['p{}{}{}{}'.format(p, l, n, c) if p>pmin else 'x' for p, l, n, c in list(itertools.product(plates, letters, nums, chans))]

slices = []
for p, l, n, c in list(itertools.product(plates, letters, nums, chans)):
    if p == start[0]:
        if letters.index(l) >= letters.index(start[1]):
            if n >= start[2]:
                slices.append('p{}{}{}{}.czi'.format(p, l, n, c))
    elif p > start[0]:
        if p < end[0]:
            slices.append('p{}{}{}{}.czi'.format(p, l, n, c))
        elif p == end[0]:
            if letters.index(l) <= letters.index(end[1]):
                if n <= end[2]:
                    slices.append('p{}{}{}{}.czi'.format(p, l, n, c))

print slices

oldDir = '/home/nick/data/jarahubdata/jarashare/histology/pinp017/orig_p1d1_p3d5'
newDir = '/home/nick/data/jarahubdata/jarashare/histology/pinp017/test'

for indf, f in enumerate(sorted(os.listdir(oldDir))):
    print slices[indf]
    shutil.copyfile(os.path.join(oldDir, f), os.path.join(newDir, slices[indf]))
