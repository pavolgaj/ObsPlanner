import stars 
import objects as objClass
import numpy as np

constellations=stars.load()
objects=objClass.objects(constellations)

f=open('stars.csv','r')
for line in f:
    if 'NAME' in line: continue
    dat=line.split(',')
    name=dat[0][1:-1].split('/')[0]
    note=dat[0][1:-1].split('/')[1] 
    tmp=dat[1].strip()[1:-1].split() 
    while len(tmp)<3: tmp.append('0')   
    ra=float(tmp[0])+float(tmp[1])/60.+float(tmp[2])/3600.
    tmp=dat[2].strip()[1:-1].split() 
    while len(tmp)<3: tmp.append('0')  
    sgn=np.sign(float(tmp[0]))
    dec=float(tmp[0])+sgn*float(tmp[1])/60.+sgn*float(tmp[2])/3600.
    #const0=dat[7]
    mag=float(dat[3].strip()[1:-1])
    typ=''
    size='' 
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

objects.save('data/objects-maxim.opd')   
         