import stars
import objects as objClass
import numpy as np
import copy
import html  #replace html characters in XML
try: import defusedxml.ElementTree as ET   #simple reading XML files
except: import xml.etree.ElementTree as ET

from tkinter import messagebox
import warnings

try: import xlwt
except:
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
        mag=dat[3].strip()[1:-1].strip()
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
    abbrevConst={x.lower():y for x,y in stars.abbrev().items()}   #malym -> osetrenie problem s velkostou pismen
    
    skratky=[x.lower() for x in constellations.keys()]        #malym -> osetrenie problem s velkostou pismen
    objects=objClass.objects(constellations)
    f=open(name,'r')
    group=''    #type of object in catalog (M,NGC etc.)
    delim=' '   #rozdelovac medzi typom (skupinou) a nazvom objektu
    for line in f:
        if len(line.strip())==0: continue #prazdny riadok
        if '[' in line:
            #rozdelenie skupin objektov v SIPS
            group=line[line.find('[')+1:line.find(']')]+delim
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
                mag=d[:d.find('m')].strip()
                continue
            except: pass
            if d.strip().lower() in skratky:
                const0=d.strip() 
                continue
            elif d.strip().lower() in abbrevConst:
                const0=abbrevConst[d.strip().lower()] 
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

def aptI(name):
    '''import objects from APT ObjectsList.xml file'''
    constellations=stars.load()
    abbrevConst={x.lower():y for x,y in stars.abbrev().items()}   #malym -> osetrenie problem s velkostou pismen
    
    objects=objClass.objects(constellations)

    xmldoc=ET.parse(name)
    objlist=xmldoc.findall('Obj')

    for obj in objlist:
        params=dict().fromkeys(['name','ra','dec','mag','size','typ','note','const'],'')
        try: params['name']=obj.find('Object').text
        except: params['name']=obj.find('Name').text 
        try: params['note']=(obj.find('NameNotes').text or '')
        except: params['note']=''
        if len(params['note'])>0: params['note']=html.unescape(params['note'])   #replace html characters in XML
        try: params['typ']=(obj.find('Type').text or '')
        except: params['typ']=''
        try: params['const']=(obj.find('Const').text or '')
        except: params['const']=''
        if params['const'].lower() in abbrevConst: params['const']=abbrevConst[params['const'].lower()]  
        try: params['mag']=obj.find('Mag').text.replace(',','.').strip()
        except AttributeError: params['mag']=''  #bez hodnoty
        try: params['size']=(obj.find('Size').text or '')
        except: params['size']=''
        try: params['ra']=stars.readDMS(obj.find('RA').text.replace(',','.'))
        except:
            messagebox.showerror('RA Format','Wrong RA format or RA not given for '+params['name']+'! Object skipped.')
            print(params['name'],'- RA:',obj.find('RA').text)
        try: params['dec']=stars.readDMS(obj.find('DEC').text.replace(',','.'))
        except:
            messagebox.showerror('DEC Format','Wrong DEC format or DEC not given for '+params['name']+'! Object skipped.')
            print(params['name'],'- DEC:',obj.find('DEC').text)

        if len(str(params['ra']))*len(str(params['dec']))==0: continue  #RA/DEC error
        objects.add(params['name'],params['ra'],params['dec'],params['mag'],params['size'],params['typ'],params['note'])
        found=False
        consts=[]
        for const in constellations:
            if constellations[const].testPoint(params['ra'],params['dec']):
                consts.append(const)
                found=True
        if not found:
            messagebox.showwarning('Constellation','Constellation of '+params['name']+'  not detected! Please, add it manually.')
            objects.objects[params['name']]['object'].const='Ari'
            print(params['name'])
        else:
            objects.objects[params['name']]['object'].const=consts[0]
            if len(consts)>1:
                messagebox.showwarning('Constellation','Multiple possible constellations for '+params['name']+' detected ('\
                +', '.join(consts)+')! Please, add it manually.')
                print(params['name'],consts)
        if (not objects.objects[params['name']]['object'].const.lower()==params['const'].lower()) and len(params['const'])>0:
            messagebox.showwarning('Constellation','Detected constellation ('+objects.objects[params['name']]['object'].const+') for '+params['name']+\
            " is different to catalog's one ("+params['const']+')! Please, add it manually.')
            print(params['name'],objects.objects[params['name']]['object'].const,params['const'])
    return objects

def plannerI(name):
    '''import objects from AstroPlanner txt file'''
    constellations=stars.load()
    abbrevConst={x.lower():y for x,y in stars.abbrev().items()}   #malym -> osetrenie problem s velkostou pismen
    objects=objClass.objects(constellations)

    xmldoc=ET.parse(name)
    objlist=xmldoc.findall('object')

    for obj in objlist:
        params=dict().fromkeys(['name','ra','dec','mag','size','typ','note','const'],'')
        params['name']=obj.find('id').text
        params['note']=(obj.find('name').text or '')
        if len(params['note'])>0: params['note']+='\n'  #uz tam daco je
        if obj.find('usernotes') is not None: params['note']+=(obj.find('usernotes').text or '')   #AP_v2
        elif obj.find('notes') is not None: params['note']+=(obj.find('notes').text or '')      #AP_v1
        if len(params['note'])>0: params['note']=html.unescape(params['note'])   #replace html characters in XML
        if obj.find('objecttype') is not None: params['typ']=(obj.find('objecttype').text or '')    #AP_v2
        elif obj.find('type') is not None: params['typ']=(obj.find('type').text or '')   #AP_v1
        params['const']=(obj.find('constellation').text or '')
        if params['const'].lower() in abbrevConst: params['const']=abbrevConst[params['const'].lower()] 
        try: params['mag']=obj.find('magnitude').text.replace(',','.').strip()
        except AttributeError: params['mag']=''  #bez hodnoty
        params['size']=(obj.find('size').text or '')
        try: params['ra']=stars.readDMS(obj.find('ra').text.replace(',','.'))
        except:
            messagebox.showerror('RA Format','Wrong RA format or RA not given for '+params['name']+'! Object skipped.')
            print(params['name'],'- RA:',obj.find('ra').text)
        try: params['dec']=stars.readDMS(obj.find('dec').text.replace(',','.'))
        except:
            messagebox.showerror('DEC Format','Wrong DEC format or DEC not given for '+params['name']+'! Object skipped.')
            print(params['name'],'- DEC:',obj.find('dec').text)

        if len(str(params['ra']))*len(str(params['dec']))==0: continue  #RA/DEC error
        objects.add(params['name'],params['ra'],params['dec'],params['mag'],params['size'],params['typ'],params['note'])
        found=False
        consts=[]
        for const in constellations:
            if constellations[const].testPoint(params['ra'],params['dec']):
                consts.append(const)
                found=True
        if not found:
            messagebox.showwarning('Constellation','Constellation of '+params['name']+'  not detected! Please, add it manually.')
            objects.objects[params['name']]['object'].const='Ari'
            print(params['name'])
        else:
            objects.objects[params['name']]['object'].const=consts[0]
            if len(consts)>1:
                messagebox.showwarning('Constellation','Multiple possible constellations for '+params['name']+' detected ('\
                +', '.join(consts)+')! Please, add it manually.')
                print(params['name'],consts)
        if (not objects.objects[params['name']]['object'].const.lower()==params['const'].lower()) and len(params['const'])>0:
            messagebox.showwarning('Constellation','Detected constellation ('+objects.objects[params['name']]['object'].const+') for '+params['name']+\
            " is different to catalog's one ("+params['const']+')! Please, add it manually.')
            print(params['name'],objects.objects[params['name']]['object'].const,params['const'])
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
        f.write('"'+str(o.mag)+'"\n')
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
        f.write(str(o.mag)+'mag\n')
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
        if 'galaxy' in o.type.lower(): typ='G'
        elif 'open' in o.type.lower(): typ='OC'
        elif 'globular' in o.type.lower(): typ='GC'
        elif 'planetary' in o.type.lower(): typ='PN'
        elif 'star' in o.type.lower(): typ='S'
        elif 'reflection' in o.type.lower(): typ='RN'
        elif 'emission' in o.type.lower(): typ='EN'
        elif 'dark' in o.type.lower(): typ='DN'
        elif 'diffuse' in o.type.lower(): typ='DFN'
        elif 'asterism' in o.type.lower(): typ='A'
        elif 'nebula' in o.type.lower(): typ='N'
        elif 'supernova' in o.type.lower(): typ='SN'
        else: 
            typ=o.type
            print(typ)
        f.write('\t\t<Type>'+typ+'</Type>\n')
        f.write('\t\t<Const>'+o.const+'</Const>\n')
        f.write('\t\t<Mag>'+str(o.mag)+'</Mag>\n')
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
        f.write(str(o.mag)+'  ')
        f.write('"'+o.size+'"  ')
        f.write('"'+o.type+'"  ')
        f.write('"'+o.note.replace('\n','; ')+'"\n')
    f.close()

def excelE(objects,name,jd,jd0,lon,lat):
    '''export objects to Excel file'''
    try: wb=xlwt.Workbook()
    except:
        messagebox.showerror('Export to Excel','Export to Excel is not possible! Please, install package "xlwt".')
        warnings.simplefilter('module')
        warnings.warn('Module "xlwt" not installed! Export to Excel will not be possible!',ImportWarning,stacklevel=2)
        return
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
        ws.write(row,7,round(o.dec+90-lat,2))
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

    return obs

def excelObsE(objects,name):
    '''export observations to Excel file'''
    try: wb=xlwt.Workbook()
    except:
        messagebox.showerror('Export to Excel','Export to Excel is not possible! Please, install package "xlwt".')
        warnings.simplefilter('module')
        warnings.warn('Module "xlwt" not installed! Export to Excel will not be possible!',ImportWarning,stacklevel=2)
        return
    ws=wb.add_sheet('Observations')
    
    time_format=xlwt.XFStyle()
    time_format.num_format_str='hh:mm:ss'
    date_format=xlwt.XFStyle()
    date_format.num_format_str='YYYY-MM-DD'
    #date_time_format=xlwt.XFStyle()
    #date_time_format.num_format_str='YYYY-MM-DD hh:mm:ss'

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
        ws.write(row,0,o.datetimeObject.date(),date_format)
        ws.write(row,1,o.datetimeObject.time(),time_format)
        #ws.write(row,19,o.datetimeObject,date_time_format)
        ws.write(row,2,o.jd)
        #ws.write(row,3,o.obj)
        #ws.write(row,4,stars.printDMS(obj.ra))
        #ws.write(row,5,stars.printDMS(obj.dec))
        #a,h=obj.altAz(o.jd,o.site.lon,o.site.lat)
        ws.write(row,3,o.obj.name)
        ws.write(row,4,stars.printDMS(o.obj.ra))
        ws.write(row,5,stars.printDMS(o.obj.dec))
        a,h=o.obj.altAz(o.jd,o.site.lon,o.site.lat)
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

    return obs

