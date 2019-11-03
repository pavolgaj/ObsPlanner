import stars 
import objects as objClass
import numpy as np

constellations=stars.load()
objects=objClass.objects(constellations)

f=open('catalog.ini','r')
for line in f:
    dat=line.split()
    name='M'+dat[0]
    ra=float(dat[1])+float(dat[2])/60.+float(dat[3])/3600.
    sgn=np.sign(float(dat[4]))
    dec=float(dat[4])+sgn*float(dat[5])/60.+sgn*float(dat[6])/3600.
    const0=dat[7]
    mag=float(dat[8][:-1])
    typ=dat[9]
    size='0'
    note=''
    if '(' in line: note=line[line.find('(')+1:line.find(')')]
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
    if not objects.objects[name]['object'].const==const0: 
        print(name,const0,objects.objects[name]['object'].const)
        objects.objects[name]['object'].const=const0
    
f.close()

objects.save('data/objects-sips.opd')   
        
