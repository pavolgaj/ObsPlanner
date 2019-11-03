import stars 
import objects as objClass
import numpy as np

constellations=stars.load()
objects=objClass.objects(constellations)

f=open('pozorovanie_V1.txt','r')     #PlainText
start=False
for line in f:
    if not start:
        if '<<Objects>>' in line: start=True
        continue
    if '<<Columns>>' in line: break
    dat=line.split('\t')
    #print(dat)
    name=dat[1].strip()
    ra=float(dat[3])
    dec=float(dat[4])
    #const0=dat[7]
    mag=float(dat[5])
    if mag>100: mag=''
    typ=dat[9].strip()
    size=dat[7].strip()
    note=dat[2].strip()
    if name==note: note=''
    #if '(' in line: note=line[line.find('(')+1:line.find(')')]
    objects.add(name,ra,dec,mag,size,typ,note)
    found=False
    consts=[]
    for const in constellations:
        if constellations[const].testPoint(ra,dec): 
            consts.append(const)
            found=True
    if not found: 
        print(name)
        objects.objects[name]['object'].const='Ari'
    else:
        objects.objects[name]['object'].const=consts[0]
        if len(consts)>1: print(name,consts)
    
f.close()

objects.save('data/objects-planner1.opd')   
        
