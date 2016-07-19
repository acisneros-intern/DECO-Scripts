import os
for (dname,dnames,fnames) in os.walk(os.getcwd()):
    for fname in fnames:
        if fname == os.path.basename(__file__) or fname == '.DS_Store':
            continue
        contents = None
        with open(fname,'r') as f:
            contents = f.readlines()
        buf = ""
        for line in contents:
            first,second = line.split(":")
            first = first.replace("{","").replace("'","").replace("\n","")
            second = second.replace("}","").replace("'","").replace("\n","").replace(" ","")
            buf += "{{'{}':'{}'}}\n".format(second,first)
        with open(fname,'w') as f:
            f.write(buf)