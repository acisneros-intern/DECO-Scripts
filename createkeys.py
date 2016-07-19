def log(*args):
    for arg in args:
        with open('keys.txt','a') as k:
            k.write(arg + "\n")
with open('justtrackpaths.out','r') as f:
    r = f.readlines()
    for i in r:
        date = i.split(" ")[-1].split("/")[-2]
        
        m = i.split(" ")[-1].split("/")[-1].replace(".jpg","_medium.png").replace("\n","")
        z = i.split(" ")[-1].split("/")[-1].replace(".jpg","_zoom.png").replace("\n","")
        
        log(str({date:m}),str({date:z}))