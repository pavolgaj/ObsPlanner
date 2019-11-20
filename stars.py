import numpy as np
import matplotlib.pyplot as mpl
import matplotlib.path as mplPath

def juldat(year,mon,day,h=0,m=0,s=0):
    '''convert date and time to julian date'''
    if mon<=2:
        year-=1
        mon+=12
    a=int(year/100)
    b=2-a+int(a/4)
    jd=int(365.25*(year+4716))+int(30.6001*(mon+1))+day+h/24.+m/1440.+s/86400.+b-1524.5
    return jd 
    
def printDMS(x):
        #output in format d:m:s
        sgn=''
        if np.sign(x)<0: sgn='-'
        x=abs(x)
        d=int(abs(x))
        m=int(round((abs(x)-d)*60.,3))
        s=abs(round((abs(x)-d-m/60.)*3600.,2))
        xx=sgn+str(d).rjust(2,'0')+':'+str(m).rjust(2,'0')+':'+('%.2f' %s).rjust(5,'0')
        return xx

def readDMS(x,deg=True):
        #input in format d:m:s
        sgn=1
        if x[0]=='-':
            sgn=-1
            x=x[1:]
        d=int(x[:x.find(':')])
        x=x[x.find(':')+1:]
        m=int(x[:x.find(':')])
        s=float(x[x.find(':')+1:])
        if deg: return sgn*(d+m/60.+s/3600.)
        else: return sgn*d,m,s

class star:
    def __init__(self,name,ra,dec,mag,size='0',typ='NA',note='',const=''):
        self.name=name
        self.ra=ra
        self.raD=ra*15
        self.dec=dec
        self.mag=mag
        self.size=size
        self.type=typ
        self.note=note
        self.const=const         
           
    def altAz(self,jd,lon,lat):        
        #type of output (same as input - number, list, numpy.array)
        out_type='lst'
        if (isinstance(jd,int) or isinstance(jd,float)): 
            #all input args are numbers        
            out_type='num' 
            
        if isinstance(jd,np.ndarray):
            #numpy.array
            out_type='np' 
            
        if isinstance(jd,list): jd=np.array(jd)
        
        #sidereal time on Greenwich in degrees or hours
        T=(jd-2451545.0)/36525
        sid=280.46061837+360.98564736629*(jd-2451545.0)+0.000387933*T**2-T**3/38710000
        sid=sid%360+lon 
    
        t=sid-self.raD        
        if out_type=='num': t=np.array([t])
        
        t=np.deg2rad(t)
        dec=np.deg2rad(self.dec)
        lat=np.deg2rad(lat)
        
        alt=np.arcsin(np.sin(dec)*np.sin(lat)+np.cos(dec)*np.cos(lat)*np.cos(t))
        sinA=np.cos(dec)*np.sin(t)/np.cos(alt)
        cosA=(-np.cos(lat)*np.sin(dec)+np.sin(lat)*np.cos(dec)*np.cos(t))/np.cos(alt)
        azm=np.arctan2(sinA,cosA)-np.pi
        azm[np.where(azm<0)]+=2*np.pi
        
        azm=np.rad2deg(azm)
        alt=np.rad2deg(alt)
    
        if out_type=='num':
            alt=alt[0]
            azm=azm[0]
        elif out_type=='lst':
            alt=alt.tolist()
            azm=azm.tolist()
        return azm,alt 
    
    def rise(self,jd,lon,lat):
        '''calculate time of rising, transit and setting; jd - at Oh UT'''
        #sidereal time on Greenwich in degrees or hours
        T=(jd-2451545.0)/36525
        sid=280.46061837+360.98564736629*(jd-2451545.0)+0.000387933*T**2-T**3/38710000
        sid=sid%360+lon             

        dec=np.deg2rad(self.dec)
        lat=np.deg2rad(lat)
        
        ha=np.arccos(-np.tan(lat)*np.tan(dec)) 
        ha=np.rad2deg(ha)
        
        t=(self.raD-sid)/15.  #transit
        t=t%24
        if np.isnan(ha): return 'NA',t,'NA'    #nie je vychod/zapad 
        r=t-ha/15.           #rise
        r=r%24
        s=t+ha/15.           #set
        s=s%24

        return r,t,s 
        
class constellation:
    def __init__(self,name):
        self.name=name
        self.stars={}
        self.lines=[]
        self.border=[[]]
        self.projection='normal'
        self.prechod=False
        
    def detect(self):
        ra=np.array([self.stars[x].ra for x in self.stars])
        dec=np.array([self.stars[x].dec for x in self.stars])      

        if np.max(np.abs(dec))>75: self.projection='polar'           
        else:            
            if np.max(ra)-np.min(ra)>12: self.prechod=True  #prechod cez 24h
    
    def plot(self,fig=None):
        '''plot starmap of constellation'''
        def transform(ra,dec):
            '''transf. coordinates for plot'''
            if self.projection=='polar':
                f=-np.deg2rad(15*ra)
                r=90-coef*dec
                ra=r*np.cos(f)
                dec=r*np.sin(f)
            if self.prechod: #prechod cez 24h
                try: 
                    if ra>12: ra-=24  
                except: ra[ra>12]-=24
            return ra,dec
        
        #stars
        ra=np.array([self.stars[x].ra for x in self.stars])
        dec=np.array([self.stars[x].dec for x in self.stars])
        mag=np.array([self.stars[x].mag for x in self.stars])  
        
        coef=1
        if fig is None: self.fig=mpl.gcf()
        else: 
            self.fig=fig
            self.fig.clf()
        self.ax=self.fig.add_subplot(111)
        
        if not self.projection=='polar': mpl.gca().invert_xaxis()         
            
        self.ax.set_yticklabels([])
        self.ax.set_xticklabels([])
        self.ax.grid(False)
        self.ax.set_axis_off()
        self.fig.tight_layout()
            
        #stars
        ra,dec=transform(ra,dec)          
        for i in np.where(mag<1): self.ax.plot(ra[i],dec[i],'k.',markersize=7)
        for i in np.where(mag<2): self.ax.plot(ra[i],dec[i],'k.',markersize=6)    
        for i in np.where(mag<3): self.ax.plot(ra[i],dec[i],'k.',markersize=4)
        for i in np.where(mag<4): self.ax.plot(ra[i],dec[i],'k.',markersize=3)
        for i in np.where(mag<5): self.ax.plot(ra[i],dec[i],'k.',markersize=2)
        self.ax.plot(ra,dec,'k.',markersize=1) 
        
        #lines
        for l in self.lines:
            for i in range(len(l)-1):
                ra0,dec0=transform(l[i][0],l[i][1])
                ra1,dec1=transform(l[i+1][0],l[i+1][1])                                            
                self.ax.plot([ra0,ra1],[dec0,dec1],'k',linewidth=0.5)
        
        #borders
        for l in self.border:
            for i in range(len(l)-1):
                ra0,dec0=transform(l[i][0],l[i][1])
                ra1,dec1=transform(l[i+1][0],l[i+1][1])                                             
                self.ax.plot([ra0,ra1],[dec0,dec1],'k--',linewidth=0.5)
            ra0,dec0=transform(l[-1][0],l[-1][1])
            ra1,dec1=transform(l[0][0],l[0][1])
            if not self.projection=='polar': self.ax.set_xlim(self.ax.get_xlim()[::-1])
            self.ax.plot([ra0,ra1],[dec0,dec1],'k--',linewidth=0.5)
            
    def testPoint(self,ra,dec):
        '''test if point is in constellation'''
        for l in self.border:
            ra0=[]
            dec0=[]
            poly=[]
            for i in l:
                ra0.append(i[0])
                dec0.append(i[1])
            ra0=np.array(ra0)
            dec0=np.array(dec0)
            if self.prechod:
                #prechod cez 24h
                ra0[ra0>12]-=24
                if ra>12: ra-=24
            if self.projection=='polar':
                if max(dec0)<0: coef=-1
                else: coef=1
                f0=-np.deg2rad(15*ra0)
                r0=90-coef*dec0
                ra0=r0*np.cos(f0)
                dec0=r0*np.sin(f0)
                
                f=-np.deg2rad(15*ra)
                r=90-coef*dec
                ra=r*np.cos(f)
                dec=r*np.sin(f)                
            for i in range(len(ra0)):
                poly.append([ra0[i],dec0[i]])
                
            if ra>max(ra0) or ra<min(ra0): continue
            if dec>max(dec0) or dec<min(dec0): continue
                    
            poly=np.array(poly)
            bbPath=mplPath.Path(poly)
        
            if bbPath.contains_point((ra,dec)): return True
        return False
    
    def plotObject(self,ra,dec,fig=None):  
        '''plot object in map'''          
        self.plot(fig)
        if self.projection=='polar':
            coef=1
            if dec<0: coef=-1
            r=90-coef*dec
            f=-np.deg2rad(15*ra)
            ra=r*np.cos(f)
            dec=r*np.sin(f)
        if self.prechod and ra>12: ra-=24
        self.ax.plot(ra,dec,'ro')

def load():        
    constellations={}

    #loading stars
    i=1
    f=open('data/stars.txt','r')
    lines=f.readlines()
    f.close()

    for line in lines:
        dat=line.split()
        const=dat[-1].strip()
        if not const in constellations: constellations[const]=constellation(const)
        constellations[const].stars[i]=star(i,float(dat[0]),float(dat[1]),float(dat[2]))
        i+=1
    #repeating stars
    constellations['Peg'].stars[1]=constellations['And'].stars[1]
    constellations['Aur'].stars[2728]=constellations['Tau'].stars[2728]
    constellations['Oph'].stars[2583]=constellations['Ser'].stars[2583]
    constellations['Oph'].stars[2602]=constellations['Ser'].stars[2602]
    constellations['Oph'].stars[2578]=constellations['Ser'].stars[2578]
        
    #nacitanie spojnic
    f=open('data/lines.txt','r')
    lines=f.readlines()
    f.close()

    old=[]        
    for l in lines:
        if l[0]=='#': 
            if not 'stop' in l:
                #new const.
                name=l[1:].strip()
                const=constellations[name]
            else:
                #stop
                const.lines.append(old)
                old=[]
            continue
                
        i=int(l)
        old.append([const.stars[i].ra,const.stars[i].dec])
    
    #load borders
    f=open('data/bound_20.dat','r')
    lines=f.readlines()
    f.close() 

    for l in lines:  
        dat=l.strip().split()
        name=dat[-1].strip()
        if len(name)==3: 
            constellations[name].border[0].append([float(dat[0]),float(dat[1])])
        else:
            i=int(name[-1])-1
            name=name[:-1]
            if len(constellations[name].border)==i: constellations[name].border.append([])
            constellations[name].border[i].append([float(dat[0]),float(dat[1])])
    
    for const in constellations: constellations[const].detect()
       
    return constellations

