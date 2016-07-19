#!/usr/bin/env python

def find_event(event,fname):
    with open(fname,'r') as f:
        ls = f.readlines()
        for l in ls:
            s_dict = eval(l)
            for i in s_dict:
                if i == event:
                    return s_dict[i]
def compare(*args):
    primary = args[0]
    signals = None
    results = {}
    with open(primary,'r') as pfile:
        signals = pfile.readlines()
    
    for signal in signals:
        s_dict = eval(signal)
        
        s_type = None
        event = None
        
        for i in s_dict:
            event = i
            s_type = s_dict[i]
            break
        
        classifications = {'Track':0,'Spot':0,'Worm':0,'Noise':0,'Other':0}
        classifications[s_type] += 1
        
        for arg in args[1:]:
            c_type = find_event(event,arg)
            classifications[c_type] += 1
        results[event] = classifications
    return results
        
        
files = ['classified_signals-owen.txt','classified_signals-valerie.txt','classified_signals-tyler.txt']
    
with open('results.txt','w') as results:
    results.write(str(len(files)) + '\n' + str(compare(*files)).replace("},","},\n"))