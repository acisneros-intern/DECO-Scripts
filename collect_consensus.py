tracks = []
with open('results.txt','r') as rfile:
    lines = rfile.readlines()
    amount = eval(lines[0])
    results = eval('\n'.join(lines[1:]))
    for item in results:
        e = results[item]
        if e['Track'] >= amount-1:
            tracks.append(item)
print len(tracks)
#print str(tracks).replace(',',',\n')