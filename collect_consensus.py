import requests
import os

FOLDER = ''
def make_folder(name,num=None):
    global FOLDER
    try:
        if num is None:
            os.mkdir(name)
            FOLDER = name
        else:
            os.mkdir("{}_{}".format(name,num))
            FOLDER = "{}_{}".format(name,num)
    except OSError:
        make_folder(name,0 if num is None else num + 1)

tracks = []
not_track = []
with open('results.txt','r') as rfile:
    lines = rfile.readlines()
    amount = eval(lines[0])
    results = eval('\n'.join(lines[1:]))
    for item in results:
        e = results[item]
        if e['Track'] == amount:
            tracks.append(item)
        elif e['Track'] == 0:
            not_track.append(item)
            
make_folder('../../../desktop/tracks')
webpath = 'https://deco-web.wipac.wisc.edu/deco_plots/'
for track in tracks:
    r = requests.get(webpath+track.replace("-","/") ,stream=True)
    if r.status_code != 200:
        print r.text
        print webpath+track.replace("-","/")    
        break
    
    with open(FOLDER+'/'+track,'w') as f:
        for chunk in r:
            f.write(chunk)