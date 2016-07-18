#!/usr/bin/env python2
import os

def log(*args):
    for arg in args:
        with open('classified_signals.txt','a') as f:
            f.write(arg)
def main(fname):
    selections = [
        "Track",
        "Worm",
        "Spot",
        "Noise",
        "Other"
    ] 
    for t in selections:
        pth = os.path.join(os.getcwd(),t)
        try:
            for (dname,dnames,fnames) in os.walk(pth):
                for f in fnames:
                    if f[-4:] == '.png':
                        log(str({t:f})+"\n")
        except OSError,e:
            print e
if __name__ == '__main__':
    main('classifications.txt')