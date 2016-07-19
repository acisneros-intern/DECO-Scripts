import os

def reconstruct(keys,item):
    for k in keys:
        if item in keys[k]:
            return "{}-{}".format(k,item)
def parse(keys):
    text = ""
    with open(keys,'r') as f:
        text = f.readlines()
    result = {}
    for k in text:
        real = eval(k)
        for val in real:
            if val in result:
                result[val].append(real[val])
            else:
                result[val] = [real[val]]
    return result
    


keys = parse('keys.txt')
for (dname,dnames,fnames) in os.walk(os.getcwd()):
    for fname in fnames:
        if 'classified_signals' in fname:
            events = None
            buf = ""
            with open(fname,'r') as f:
                events = f.readlines()
            for e in events:
                d = eval(e)
                for i in d:
                    name = d[i]
                    buf += str({reconstruct(keys,i):name}) + "\n"
            with open(fname,'w') as f:
                f.write(buf)