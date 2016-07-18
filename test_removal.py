import os
from PIL import Image
import sys
pth = '/users/cisnerosa/desktop/classification/track/'
count = 0
def distance(*args):
    total = 0
    for (index,num) in enumerate(args[1:]):
        diff = abs(num - args[index])
        total += diff
    return total
for (dname,dnames,fnames) in os.walk(pth):
    for fname in fnames:
        if fname[-4:] != '.png':
            continue
        im = Image.open(pth+fname)
        px = im.load()
        
        width,height = im.size
        for y in range(height):
            for x in range(width):
                r,g,b,a = px[x,y]
                if distance(r,g,b) < 30:
                    px[x,y] = (0,0,0,255)
        im.save('/users/cisnerosa/desktop/filtering/'+fname)
        sys.stdout.write("\r("+str(count).zfill(3)+") "+str(int(count/560.0*100)).zfill(2)+"%")
        sys.stdout.flush()
        count += 1