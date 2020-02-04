import stars
import objects as objClass
import numpy as np
import copy

from tkinter import messagebox

try: import xlwt
except:
    import warnings
    warnings.simplefilter('module')
    warnings.warn('Module "xlwt" not installed! Export to Excel will not be possible!',ImportWarning,stacklevel=2)

class siteClass():
    def __init__(self,name,lat,lon,ele,limits=None):
        self.name=name
        self.lat=lat
        self.lon=lon
        self.ele=ele
        if limits is None: self.limits=[0,90,0,360]     #min_alt,max_alt,min_az,max_az
        else: self.limits=limits

def sortObs(zoznam):
    #sort observations by JulDate
    obsSort=[]
    order={}
    for x in zoznam:
        if zoznam[x].jd in order:
            off=1e-10
            while zoznam[x].jd+off in order: off+=1e-10
            order[zoznam[x].jd+off]=x
        else: order[zoznam[x].jd]=x
    for x in sorted(order): obsSort.append(order[x])
    return obsSort

def join(name1,name2,save=False):
    '''join 2 objects files'''
    constellations=stars.load()

    objects1=objClass.objects(constellations)
    objects1.load(name1)

    objects2=objClass.objects(constellations)
    objects2.load(name2)

    for obj in objects2.objects:
        if obj in objects1.objects:
            print(obj,'is already in file.')
            continue
        objects1.objects[obj]=objects2.objects[obj]

    if save: objects1.save(name1)
    return objects1

#todo: const not found -> warning/error?

def maximI(name):
    '''import objects from MaximDL file'''
    constellations=stars.load()
    objects=objClass.objects(constellations)
    f=open(name,'r')
    for line in f:
        if 'NAME' in line: continue
        if len(line.strip())==0: continue #prazdny riadok
        dat=line.split(',')
        name=dat[0][1:-1].split('/')[0]
        note=dat[0][1:-1].split('/')[1]
        tmp=dat[1].strip()[1:-1].split()
        while len(tmp)<3: tmp.append('0')
        ra=float(tmp[0])+float(tmp[1])/60.+float(tmp[2])/3600.
        tmp=dat[2].strip()[1:-1].split()
        while len(tmp)<3: tmp.append('0')
        if '-' in tmp[0]: sgn=-1
        else: sgn=1
        dec=float(tmp[0])+sgn*float(tmp[1])/60.+sgn*float(tmp[2])/3600.
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
            messagebox.showwarning('Constellation','Constellation of '+name+'  not detected! Please, add it manually.')
            objects.objects[name]['object'].const='Ari'
            print(name)
        else:
            objects.objects[name]['object'].const=consts[0]
            if len(consts)>1:
                messagebox.showwarning('Constellation','Multiple possible constellations for '+name+' detected ('\
                +', '.join(consts)+')! Please, add it manually.')
                print(name,consts)
    f.close()
    return objects

def sipsI(name):
    '''import objects from SIPS file'''
    constellations=stars.load()
    skratky=[x.lower() for x in constellations.keys()]        #malym -> osetrenie problem s velkostou pismen
    objects=objClass.objects(constellations)
    f=open(name,'r')
    group=''    #type of object in catalog (M,NGC etc.)
    for line in f:
        if len(line.strip())==0: continue #prazdny riadok
        if '[' in line:
            #rozdelenie skupin objektov v SIPS
            group=line[line.find('[')+1:line.find(']')]+' '
            continue
        dat=line.split()
        name=group+dat[0].strip()
        ra=float(dat[1])+float(dat[2])/60.+float(dat[3])/3600.
        if '-' in dat[4]: sgn=-1
        else: sgn=1
        dec=float(dat[4])+sgn*float(dat[5])/60.+sgn*float(dat[6])/3600.
        const0=''
        mag=''
        typ=''
        for d in dat[7:]:
            #osetrenie nahodneho usporiadania stlpcov v SIPS!!!!
            try:
                mag=float(d[:d.find('m')])
                continue
            except: pass
            if d.strip().lower() in skratky:
                const0=d.strip()
                continue
            typ=d
        size=''
        if '(' in line: note=line[line.find('(')+1:line.find(')')]
        else: note=''
        objects.add(name,ra,dec,mag,size,typ,note)
        found=False
        consts=[]
        for const in constellations:
            if constellations[const].testPoint(ra,dec):
                consts.append(const)
                found=True
        if not found:
            messagebox.showwarning('Constellation','Constellation for '+name+' not detected! Please, add it manually.')
            objects.objects[name]['object'].const='Ari'
            print(name)
        else:
            objects.objects[name]['object'].const=consts[0]
            if len(consts)>1:
                messagebox.showwarning('Constellation','Multiple possible constellations for '+name+' detected ('\
                +', '.join(consts)+')! Please, add it manually.')
                print(name,consts)
        if (not objects.objects[name]['object'].const.lower()==const0.lower()) and len(const0)>0:
            messagebox.showwarning('Constellation','Detected constellation ('+objects.objects[name]['object'].const+') for '+name+\
            " is different to catalog's one ("+const0+')! Please, add it manually.')
            print(name,objects.objects[name]['object'].const,const0)
    f.close()
    return objects

def maximE(objects,name):
    '''export objects to MaximDL file'''
    f=open(name,'w')
    f.write('"NAME","R.A.","DEC.","MAG"\n')
    for i in objects:
        o=objects[i]['object']
        f.write('"'+o.name+'/",')
        f.write('"'+stars.printDMS(o.ra).replace(':',' ')+'",')
        f.write('"'+stars.printDMS(o.dec).replace(':',' ')+'",')
        f.write('"'+o.mag+'"\n')
    f.close()

def sipsE(objects,name):
    '''export objects to SIPS file'''
    f=open(name,'w')
    f.write('[objects]\n')
    for i in objects:
        o=objects[i]['object']
        f.write(o.name.replace(' ','_')+' ')
        f.write(stars.printDMS(o.ra).replace(':',' ')+' ')
        f.write(stars.printDMS(o.dec).replace(':',' ')+' ')
        f.write(o.const+' ')
        f.write(o.type.replace(' ','_')+' ')
        f.write(o.size.replace(' ','_')+' ')
        f.write(o.mag+'mag\n')
    f.close()

def aptE(objects,name):
    '''export objects to APT file'''
    f=open(name,'w')
    f.write('<?xml version="1.0"?>\n<Objects>\n')
    for i in objects:
        o=objects[i]['object']
        f.write('\t<Obj>\n')
        f.write('\t\t<Object>'+o.name+'</Object>\n')
        f.write('\t\t<NameNotes>'+o.note.replace('\n','; ')+'</NameNotes>\n')
        f.write('\t\t<Type>'+'</Type>\n')
        f.write('\t\t<Const>'+o.const+'</Const>\n')
        f.write('\t\t<Mag>'+o.mag+'</Mag>\n')
        f.write('\t\t<Size>'+o.size.replace("'",'')+'</Size>\n')
        f.write('\t\t<RA>'+stars.printDMS(o.ra)+'</RA>\n')
        f.write('\t\t<DEC>'+stars.printDMS(o.dec)+'</DEC>\n')
        f.write('\t\t<Angle></Angle>\n')
        f.write('\t</Obj>\n')
    f.write('</Objects>\n')
    f.close()

def textE(objects,name):
    '''export objects to Text file'''
    f=open(name,'w')
    f.write('"Name"  RA  Dec  Const.  Mag  "Size"  "Type"  "Note"\n')
    for i in objects:
        o=objects[i]['object']
        f.write('"'+o.name+'"  ')
        f.write(stars.printDMS(o.ra)+'  ')
        f.write(stars.printDMS(o.dec)+'  ')
        f.write(o.const+'  ')
        f.write(o.mag+'  ')
        f.write('"'+o.size+'"  ')
        f.write('"'+o.type+'"  ')
        f.write('"'+o.note.replace('\n','; ')+'"\n')
    f.close()

def excelE(objects,name,jd,jd0,lon,lat):
    '''export objects to Excel file'''
    wb=xlwt.Workbook()
    ws=wb.add_sheet('Objects')

    ws.write(0,0,'Name')
    ws.write(0,1,'RA')
    ws.write(0,2,'DEC')
    ws.write(0,3,'Alt.')
    ws.write(0,4,'Azm.')
    ws.write(0,5,'Rise')
    ws.write(0,6,'Transit')
    ws.write(0,7,'Transit Alt.')
    ws.write(0,8,'Set')
    ws.write(0,9,'Const.')
    ws.write(0,10,'Mag')
    ws.write(0,11,'Size')
    ws.write(0,12,'Type')
    ws.write(0,13,'Note')
    for i in range(14): ws.col(i).width=3500
    row=1
    for i in objects:
        o=objects[i]['object']
        ws.write(row,0,o.name)
        ws.write(row,1,stars.printDMS(o.ra))
        ws.write(row,2,stars.printDMS(o.dec))
        a,h=o.altAz(jd,lon,lat)
        ws.write(row,3,stars.printDMS(h))
        ws.write(row,4,stars.printDMS(a))
        r,t,s=o.rise(jd0,lon,lat)
        if not r=='NA':
            r=stars.printDMS(r)
            s=stars.printDMS(s)
        ws.write(row,5,r)
        ws.write(row,6,stars.printDMS(t))
        ws.write(row,7,o.dec+90-lat)
        ws.write(row,8,s)
        ws.write(row,9,o.const)
        try: ws.write(row,10,float(o.mag))
        except: ws.write(row,10,o.mag)
        ws.write(row,11,o.size)
        ws.write(row,12,o.type)
        ws.write(row,13,o.note.replace('\n','; '))
        row+=1
    wb.save(name)

def textObsE(objects,name):
    '''export observations to Text file'''
    f=open(name,'w')
    f.write('Date  Time  "Object"  "Observer"  "Telescope"  "Site"  Long.  Lat.  Elev. "Note"\n')
    obs={}  #list of all observations
    for i in objects:
        o=objects[i]['obs']
        for j in o:
            if j in obs:
                #multiple objects observed at same time
                off=1
                while j+str(off) in obs: off+=1
                obs[j+str(off)]=o[j]
            else: obs[j]=o[j]
    #sort by Object and JD
    #for i in objects:
    #    AllObs=objects[i]['obs']
    #    for j in sortObs(AllObs):
    #        o=AllObs[j]

    #sort all observations by JD
    for i in sortObs(obs):
        o=obs[i]
        f.write(o.date.replace(" ","  ")+'  ')
        f.write('"'+o.obj+'"  ')
        f.write('"'+o.observer+'"  ')
        f.write('"'+o.telescope+'"  ')
        f.write('"'+o.site.name+'"  ')
        f.write(stars.printDMS(o.site.lon)+'  ')
        f.write(stars.printDMS(o.site.lat)+'  ')
        f.write(str(o.site.ele)+'  ')
        f.write('"'+o.note.replace('\n','; ')+'"\n')
    f.close()

def excelObsE(objects,name):
    '''export observations to Excel file'''
    wb=xlwt.Workbook()
    ws=wb.add_sheet('Observations')

    ws.write(0,0,'Date')
    ws.write(0,1,'Time')
    ws.write(0,2,'JulDat')
    ws.write(0,3,'Object')
    ws.write(0,4,'RA')
    ws.write(0,5,'DEC')
    ws.write(0,6,'Alt.')
    ws.write(0,7,'Azm.')
    ws.write(0,8,'Const.')
    ws.write(0,9,'Mag')
    ws.write(0,10,'Size')
    ws.write(0,11,'Type')
    ws.write(0,12,'Observer')
    ws.write(0,13,'Telescope')
    ws.write(0,14,'Site')
    ws.write(0,15,'Long.')
    ws.write(0,16,'Lat.')
    ws.write(0,17,'Elev.')
    ws.write(0,18,'Note')

    for i in range(19): ws.col(i).width=3500
    row=1

    obs={}  #list of all observations
    for i in objects:
        o=objects[i]['obs']
        obj=objects[i]['object']
        for j in o:
            if j in obs:
                #multiple objects observed at same time
                off=1
                while j+str(off) in obs: off+=1
                obs[j+str(off)]=copy.deepcopy(o[j])
                obs[j+str(off)].obj=obj
            else:
                obs[j]=copy.deepcopy(o[j])
                obs[j].obj=obj
    #sort by Object and JD
    #for i in objects:
    #     AllObs=objects[i]['obs']
    #     obj=objects[i]['object']
    #     for j in sortObs(AllObs):
    #         o=AllObs[j]

    #sort all observations by JD
    for i in sortObs(obs):
        o=obs[i]
        ws.write(row,0,o.date.split()[0])
        ws.write(row,1,o.date.split()[1])
        ws.write(row,2,o.jd)
        #ws.write(row,3,o.obj)
        #ws.write(row,4,stars.printDMS(obj.ra))
        #ws.write(row,5,stars.printDMS(obj.dec))
        #a,h=obj.altAz(o.jd,o.site.lon,o.site.lat)
        ws.write(row,3,o.obj.name)
        ws.write(row,4,stars.printDMS(o.obj.ra))
        ws.write(row,5,stars.printDMS(o.obj.dec))
        a,h=obj.altAz(o.jd,o.site.lon,o.site.lat)
        ws.write(row,6,stars.printDMS(h))
        ws.write(row,7,stars.printDMS(a))
        #ws.write(row,8,obj.const)
        #try: ws.write(row,9,float(obj.mag))
        #except: ws.write(row,9,obj.mag)
        #ws.write(row,10,obj.size)
        #ws.write(row,11,obj.type)
        ws.write(row,8,o.obj.const)
        try: ws.write(row,9,float(o.obj.mag))
        except: ws.write(row,9,o.obj.mag)
        ws.write(row,10,o.obj.size)
        ws.write(row,11,o.obj.type)
        ws.write(row,12,o.observer)
        ws.write(row,13,o.telescope)
        ws.write(row,14,o.site.name)
        ws.write(row,15,stars.printDMS(o.site.lon))
        ws.write(row,16,stars.printDMS(o.site.lat))
        ws.write(row,17,o.site.ele)
        ws.write(row,18,o.note.replace('\n','; '))
        row+=1
    wb.save(name)

