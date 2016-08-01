from skimage import measure
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpim
from itertools import izip
import math
import sys
import time

def distance(*args):
    """
    Cumulative distance between values in a list
    """
    total = 0
    for (index,num) in enumerate(args[1:]):
        total += abs(args[index]-num)
    return total
def polygon_area(x,y):
    #find the area of a polygon given it's vertices, takes two 1d arrays of x and y coordinates like: (0,1,2,3) (0,1,2,3)
    area = 0
    j = len(x)-1
    
    for i in range(j+1):
        area += (x[j] + x[i]) * (y[j] - y[i])
        j = i
    return abs(area/2.0)
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
    three_over_255 = 0.0117647058824
    for y in range(size[1]):
        row = []
        for x in range(size[0]):
            r,g,b,a = image[x,y]
            av = (r+g+b)/ three_over_255
            if distance(r,g,b) < 25: #or distance(r,g,b) < 25:
                av = 0.0
            row.append(av)
            avg += av
        result.append(row)
        
    avg /= float(size[0] * size[1])
    return result,avg
def log(info):
    """
    write 'info' to 'log.txt'
    """
    with open('log.txt','a') as f:
        f.write('\n{}'.format(info))
        
def process(name,target_size):
    global DESTINATION
    im = crop(name)
    w,h = im.size
    
    px = im.load()
    im_arr,avg = to_array(px,(w,h))

    npim = np.array(im_arr,dtype=float)
    
    cc = measure.find_contours(npim,avg*10)
    
    #display in pyplot
   # plt.imshow(im)
    
    #find largest and smallest point in order to create bbox
    largest = [0,0]
    smallest = [w,h]
    
    #find the largest contour, and choose that to crop the image
    contour_choices = []
    for c in cc:
        contour_choices.append(polygon_area(c[:,1],c[:,0]))
    optimal = contour_choices.index(max(contour_choices))
       
    #find the bounding box of the chosen contour for cropping 
    for i in range(len(cc[optimal][:,1])):
        x = cc[optimal][:,1][i]
        y = cc[optimal][:,0][i]

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
    im.thumbnail(target_size)
    im = im.convert('L')
    
    im.save('{}/{}'.format(DESTINATION,name.split("/")[-1]))


DESTINATION = '/users/cisnerosa/desktop/track_sample/'
SOURCE = '/Users/cisnerosa/Desktop/tracks/'
def main():
    global SOURCE
    pth = SOURCE
    count = 0
    FAILURES = 0
    failed_files = []
    start = time.time()
    times = []
    for (dname,dnames,fnames) in os.walk(pth):
        total = len(fnames)
        for fname in fnames:
            count += 1
            if fname [-4:] != '.png':
                continue
            sys.stdout.write("\r{}/{}({}%)".format(str(count).zfill(3),total,str(int(float(count)/float(total)*100)).zfill(3)))
            sys.stdout.flush()
            try:
                t = time.time()
                process(pth+fname,(32,32))
                e = time.time() - t
                times.append(e)
            except Exception, e:
                print e
                failed_files.append(fname)
                FAILURES += 1
        success = float(total - FAILURES)
        elapsed = time.time() - start
        minutes, seconds = (int(math.floor(elapsed/60)),float("{0:.2f}".format(elapsed % 60)))
        log((minutes,seconds))
        print "\n {} minutes {} seconds total. {} seconds each.\n".format(minutes,seconds,elapsed/total)
        print "{} completed. {} guaranteed failures. Maximum {}% success rate.".format(total,FAILURES,int(success/total*100))
        
        plt.plot(times)
        avg = range(total)
        for (index,a) in enumerate(avg): avg[index] = elapsed / total
        plt.plot(avg)
        plt.ylabel('processing time (seconds)')
        plt.xlabel('samples')
        plt.show()
if __name__ == '__main__':
    main()            