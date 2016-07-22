import os
from PIL import Image
import sys
import time
import math

pth = '/Users/cisnerosa/Desktop/classification/unanimous_tracks/'
count = 0
def distance(*args):
    total = 0
    for (index,num) in enumerate(args[1:]):
        diff = abs(num - args[index])
        total += diff
    return total
def crop(fname):
    # takes a filename 'image' and crops it by 100,100,100,175. Returns this as a PhotoImage for use with tk canvas .

    image = Image.open(fname)
    c = (100,100,image.width-100,image.height-175)
    image = image.crop(c)
    return image
    
    
distance_threshold = 25
start = time.time()
for (dname,dnames,fnames) in os.walk(pth):
    total = float(len(fnames))
    for fname in fnames:
        if fname[-4:] != '.png':
            continue
        im = crop(pth+fname)
        px = im.load()
        
        width,height = im.size
        for y in range(height):
            for x in range(width):
                r,g,b,a = px[x,y]
                if distance(r,g,b) < distance_threshold:
                    px[x,y] = (0,0,0,255)
        im.save('/users/cisnerosa/desktop/filtering/'+fname)
        sys.stdout.write("\r("+str(count).zfill(3)+") "+str(int(count/total*100)).zfill(2)+"%")
        sys.stdout.flush()
        count += 1
elapsed = time.time() - start
minutes, seconds = (int(math.floor(elapsed/60)),float("{0:.2f}".format(elapsed % 60)))
print "\n{} minutes {} seconds elapsed\n".format(minutes,seconds)