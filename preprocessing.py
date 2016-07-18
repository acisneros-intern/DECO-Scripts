from skimage import measure
import os
from PIL import Image
import numpy as np
#import matplotlib.pyplot as plt
import matplotlib.image as mpim
from itertools import izip
import math
import sys
import time

def distance(*args):
    total = 0
    for (index,num) in enumerate(args[1:]):
        total += abs(args[index]-num)
    return total
        
def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)
def crop(fname):
    # takes a filename 'image' and crops it by 100,100,100,175. Returns this as a PhotoImage for use with tk canvas .

    image = Image.open(fname)
    c = (100,100,image.width-100,image.height-175)
    image = image.crop(c)
    return image
def to_array(image,size):
    result = []
    avg = 0
    
    for y in range(size[1]):
        row = []
        for x in range(size[0]):
            r,g,b,a = image[x,y]
            av = (r+g+b)/3.0/255.0
            if (r,g,b) == (255,255,255): #or distance(r,g,b) < 25:
                av = 0.0
            row.append(av)
            avg += av
        result.append(row)
        
    avg /= float(size[0] * size[1])
    return result,avg
def magnitude(p0,p1):
    a = p0[0] - p1[0]
    b = p0[1] - p1[0]
    return math.sqrt()
def log(info):
    with open('log.txt','a') as f:
        f.write('\n{}'.format(info))
def process(name,target_size):
    im = Image.open(name)
    w,h = im.size
    
    px = im.load()
    im_arr,avg = to_array(px,(w,h))

    npim = np.array(im_arr,dtype=float)
    
    cc = measure.find_contours(npim,avg*10)
    
    #display in pyplot
   # pyim = plt.imread(name)
   # plt.imshow(pyim)
    
    #find largest and smallest point in order to create bbox
    largest = [0,0]
    smallest = [w,h]
    
    for i in range(len(cc[0][:,1])):
        x = cc[0][:,1][i]
        y = cc[0][:,0][i]

        # im.putpixel((x,y),(30,200,100))
        if x < smallest[0]:
            smallest[0] = x
        if y < smallest[1]:
            smallest[1] = y
        if x > largest[0]:
            largest[0] = x
        if y > largest[1]:
            largest[1] = y
            
            
    
    #crop image so only event is visible and save
    
    im = im.crop((smallest[0],smallest[1],largest[0],largest[1]))
    im.save('/users/cisnerosa/desktop/results/{}'.format(name.split("/")[-1]))
    
    #plt.plot(cc[0][:, 1], cc[0][:, 0], linewidth=2)
    
    #plt.show()
    
pth = '/Users/cisnerosa/Desktop/classification/Track/'
count = 0
FAILURES = 0
failed_files = []
start = time.time()
for (dname,dnames,fnames) in os.walk(pth):
    total = len(fnames)
    for fname in fnames:
        count += 1
        if fname [-4:] != '.png':
            continue
        sys.stdout.write("\r{}/{}({}%)".format(str(count).zfill(3),total,str(int(float(count)/float(total)*100)).zfill(3)))
        sys.stdout.flush()
        try:
            process(pth+fname,(32,32))
        except:
            failed_files.append(fname)
            FAILURES += 1
    success = float(total - FAILURES)
    elapsed = time.time() - start
    print "\n {} minutes {} seconds\n".format(int(math.floor(elapsed/60)),"{0:.2f}".format(elapsed % 60))
    print "{} completed. {} guaranteed failures. Maximum {}% success rate.".format(total,FAILURES,int(success/total*100))
    for f in failed_files:
        os.system('open {}'.format(pth+f))

        
        
        
        
        
                