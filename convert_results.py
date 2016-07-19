#!/usr/bin/env python2
import os

def log(*args):
    for arg in args:
        with open('classified_signals.txt','a') as f:
            f.write(arg)
def main():
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
                        log(str({f:t})+"\n")
        except OSError,e:
            print e
if __name__ == '__main__':
    main()