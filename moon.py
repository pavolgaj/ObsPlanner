import numpy as np
import datetime
from stars import sid_time

def jd2date(jd):
    '''convert julian date to date and time'''
    jd+=0.5
    z=int(jd)
    f=jd%1
    if z<2299161: a=z
    else:
        alp=int((z-1867216.25)/36524.25)
        a=z+1+alp-int(alp/4)
    b=a+1524
    c=int((b-122.1)/365.25)
    d=int(365.25*c)
    e=int((b-d)/30.6001)

    h=int(f*24)
    m=int((f-h/24.)*1440)
    s=int((f-h/24.-m/1440.)*86400.)
    day=b-d-int(30.6001*e)
    if  e<14: mon=e-1
    else: mon=e-13
    if mon>2: year=c-4716
    else: year=c-4715

    return datetime.datetime(year,mon,day,h,m,s)

def sunCoordinates(jd):
    '''equatorial coordinates of Sun'''
    T=(jd-2451545)/36525.
    L=np.deg2rad(280.46646+36000.76983*T+0.0003032*T**2)
    M=np.deg2rad(357.52911+35999.05029*T-0.0001537*T**2)
    C=np.deg2rad((1.914602-0.004817*T-0.000014*T**2)*np.sin(M)+(0.019993-0.000101*T)*np.sin(2*M)+0.000289*np.sin(3*M))

    lon=L+C

    U=T/100.
    eps=np.deg2rad(23+26/60.+(21.448-4680.93*U-1.55*U**2+1999.25*U**3-51.38*U**4-249.67*U**5-39.05*U**6+7.12*U**7+27.87*U**8+5.79*U**9+2.45*U**10)/3600.)

    ra=np.rad2deg(np.arctan2(np.cos(eps)*np.sin(lon),np.cos(lon)))
    de=np.rad2deg(np.arcsin(np.sin(eps)*np.sin(lon)))
    return ra,de


def moonCoordinates(jd):
    '''equatorial geocentric coordinates of Moon'''
    T=(jd-2451545)/36525.

    L=np.deg2rad(218.3164477+481267.88123421*T-0.0015786*T**2+T**3/538841.-T**4/65194000.)
    D=np.deg2rad(297.8501921+445267.1114034*T-0.0018819*T**2+T**3/545868.-T**4/113065000.)
    M=np.deg2rad(357.5291092+35999.0502909*T-0.0001536*T**2+T**3/24490000.)
    Mm=np.deg2rad(134.9633964+477198.8675055*T+0.0087414*T**2+T**3/69699.-T**4/14712000.)
    W=np.deg2rad(125.04452-1934.136261*T+0.0020708*T**2+T**3/450000.)
    F=np.deg2rad(93.2720950+483202.0175233*T-0.0036539*T**2-T**3/3526000.+T**4/863310000.)

    A1=np.deg2rad(119.75+131.849*T)
    A2=np.deg2rad(53.09+479264.290*T)
    A3=np.deg2rad(313.45+481266.484*T)

    E=1-0.002516*T-0.0000047*T**2

    args=np.array([[0,0,1,0],[2,0,-1,0],[2,0,0,0],[0,0,2,0],[0,1,0,0],[0,0,0,2],[2,0,-2,0],[2,-1,-1,0],[2,0,1,0],[2,-1,0,0],[0,1,-1,0],[1,0,0,0],[0,1,1,0],[2,0,0,-2],[0,0,1,2],[0,0,1,-2],[4,0,-1,0],\
          [0,0,3,0],[4,0,-2,0],[2,1,-1,0],[2,1,0,0],[1,0,-1,0],[1,1,0,0],[2,-1,1,0],[2,0,2,0],[4,0,0,0],[2,0,-3,0],[0,1,-2,0],[2,0,-1,2],[2,-1,-2,0],[1,0,1,0],[2,-2,0,0],[0,1,2,0],[0,2,0,0],\
          [2,-2,-1,0],[2,0,1,-2],[2,0,0,2],[4,-1,-1,0],[0,0,2,2],[3,0,-1,0],[2,1,1,0],[4,-1,-2,0],[0,2,-1,0],[2,2,-1,0],[2,1,-2,0],[2,-1,0,-2],[4,0,1,0],[0,0,4,0],[4,-1,0,0],[1,0,-2,0],\
          [2,1,0,-2],[0,0,2,-2],[1,1,1,0],[3,0,-2,0],[4,0,-3,0],[2,-1,2,0],[0,2,1,0],[1,1,-1,0],[2,0,3,0],[2,0,-1,-2]])
    argsb=np.array([[0,0,0,1],[0,0,1,1],[0,0,1,-1],[2,0,0,-1],[2,0,-1,1],[2,0,-1,-1],[2,0,0,1],[0,0,2,1],[2,0,1,-1],[0,0,2,-1],[2,-1,0,-1],[2,0,-2,-1],[2,0,1,1],[2,1,0,-1],[2,-1,-1,1],[2,-1,0,1],\
          [2,-1,-1,-1],[0,1,-1,-1],[4,0,-1,-1],[0,1,0,1],[0,0,0,3],[0,1,-1,1],[1,0,0,1],[0,1,1,1],[0,1,1,-1],[0,1,0,-1],[1,0,0,-1],[0,0,3,1],[4,0,0,-1],[4,0,-1,1],[0,0,1,-3],[4,0,-2,1],\
          [2,0,0,-3],[2,0,2,-1],[2,-1,1,-1],[2,0,-2,1],[0,0,3,-1],[2,0,2,1],[2,0,-3,-1],[2,1,-1,1],[2,1,0,1],[4,0,0,1],[2,-1,1,1],[2,-2,0,-1],[0,0,1,3],[2,1,1,-1],[1,1,0,-1],[1,1,0,1],\
          [0,1,-2,-1],[2,1,-1,-1],[1,0,1,1],[2,-1,-2,-1],[0,1,2,1],[4,0,-2,-1],[4,-1,-1,-1],[1,0,1,-1],[4,0,1,-1],[1,0,-1,-1],[4,-1,0,-1],[2,-2,0,1]])
    args1=np.array([D,M,Mm,F])

    sinC=np.array([6288774,1274027,658314,213618,-185116,-114332,58793,57066,53322,45758,-40923,-34720,-30383,15327,-12528,10980,10675,10034,8548,-7888,-6766,-5163,4987,4036,3994,3861,3665,-2689,-2602,\
        2390,-2348,2236,-2120,-2069,2048,-1773,-1595,1215,-1110,-892,-810,759,-713,-700,691,596,549,537,520,-487,-399,-381,351,-340,330,327,-323,299,294,0])
    bC=np.array([5128122,280602,277693,173237,55413,46271,32573,17198,9266,8822,8216,4324,4200,-3359,2463,2211,2065,-1870,1828,-1794,-1749,-1565,-1491,-1475,-1410,-1344,-1335,1107,1021,833,777,671,607,\
        596,491,-451,439,422,421,-366,-351,331,315,302,-283,-229,223,223,-220,-220,-185,181,-177,176,166,-164,132,-119,115,107])

    coefE=np.ones(sinC.shape)
    coefE[np.where(args[:,1]==1)]=E
    coefE[np.where(args[:,1]==1)]=E**2
    l=np.sum(sinC*coefE*np.sin(np.sum(args*args1,axis=1)))+3958*np.sin(A1)+1962*np.sin(L-F)+318*np.sin(A2)

    coefE=np.ones(sinC.shape)
    coefE[np.where(argsb[:,1]==1)]=E
    coefE[np.where(argsb[:,1]==1)]=E**2
    b=np.sum(bC*coefE*np.sin(np.sum(argsb*args1,axis=1)))-2235*np.sin(L)+382*np.sin(A3)+175*np.sin(A1-F)+175*np.sin(A1+F)+127*np.sin(L-Mm)-115*np.sin(L+Mm)

    lon=(np.rad2deg(L)+l/1e6)%360
    lat=b/1e6

    #calculate nutation in longitude (psi) and obliquity (eps), in degrees
    args=np.array([[0,0,0,0,1],[-2,0,0,2,2],[0,0,0,2,2],[0,0,0,0,2],[0,1,0,0,0],[0,0,1,0,0],[-2,1,0,2,2],[0,0,0,2,1],[0,0,1,2,2],[-2,-1,0,2,2],[-2,0,1,0,0],[-2,0,0,2,1],[0,0,-1,2,2],[2,0,0,0,0],\
        [0,0,1,0,1],[2,0,-1,2,2],[0,0,-1,0,1],[0,0,1,2,1],[-2,0,2,0,0],[0,0,-2,2,1],[2,0,0,2,2],[0,0,2,2,2],[0,0,2,0,0],[-2,0,1,2,2],[0,0,0,2,0],[-2,0,0,2,0],[0,0,-1,2,1],[0,2,0,0,0],\
        [2,0,-1,0,1],[-2,2,0,2,2],[0,1,0,0,1],[-2,0,1,0,1],[0,-1,0,0,1],[0,0,2,-2,0],[2,0,-1,2,1],[2,0,1,2,2],[0,1,0,2,2],[-2,1,1,0,0],[0,-1,0,2,2],[2,0,0,2,1],[2,0,1,0,0],[-2,0,2,2,2],\
        [-2,0,1,2,1],[2,0,-2,0,1],[2,0,0,0,1],[0,-1,1,0,0],[-2,-1,0,2,1],[-2,0,0,0,1],[0,0,2,2,1],[-2,0,2,0,1],[-2,1,0,2,1],[0,0,1,-2,0],[-1,0,1,0,0],[-2,1,0,0,0],[1,0,0,0,0],[0,0,1,2,0],\
        [0,0,-2,2,2],[-1,-1,1,0,0],[0,1,1,0,0],[0,-1,1,2,2],[2,-1,-1,2,2],[0,0,3,2,2],[2,-1,0,2,2]])
    args1=np.array([D,M,Mm,F,W])
    sinC=np.array([-171996-174.2*T,-13187-1.6*T,-2274-0.2*T,2062+0.2*T,1426-3.4*T,712+0.1*T,-517+1.2*T,-386-0.4*T,-301,217-0.5*T,-158,129+0.1*T,123,63,63+0.1*T,-59,-58-0.1*T,-51,48,46,-38,-31,29,29,26,\
        -22,21,17-0.1*T,16,-16+0.1*T,-15,-13,-12,11,-10,-8,7,-7,-7,-7,6,6,6,-6,-6,5,-5,-5,-5,4,4,4,-4,-4,-4,3,-3,-3,-3,-3,-3,-3,-3])
    cosC=np.array([92025+8.9*T,5736-3.1*T,977-0.5*T,-895+0.5*T,54-0.1*T,-7,224-0.6*T,200,129-0.1*T,-95+0.3*T,0,-70,-53,0,-33,26,32,27,0,-24,16,13,0,-12,0,0,-10,0,-8,7,9,7,6,0,5,3,-3,0,3,3,0,-3,-3,3,3,0,\
        3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

    psi=np.sum(sinC*np.sin(np.sum(args*args1,axis=1)))
    U=T/100.

    eps=23+26/60.+(21.448-4680.93*U-1.55*U**2+1999.25*U**3-51.38*U**4-249.67*U**5-39.05*U**6+7.12*U**7+27.87*U**8+5.79*U**9+2.45*U**10)/3600.
    eps+=np.sum(cosC*np.cos(np.sum(args*args1,axis=1)))/1e4/3600.

    psi=psi/1e4/3600.
    eps=np.deg2rad(eps)
    lon+=psi

    lam=np.deg2rad(lon)
    beta=np.deg2rad(lat)

    dec=np.arcsin(np.sin(beta)*np.cos(eps)+np.cos(beta)*np.sin(eps)*np.sin(lam))
    sinR=(np.sin(lam)*np.cos(beta)*np.cos(eps)-np.sin(beta)*np.sin(eps))/np.cos(dec)
    cosR=np.cos(lam)*np.cos(beta)/np.cos(dec)

    ra=np.arctan2(sinR,cosR)
    if ra<0: ra+=2*np.pi

    ra=np.rad2deg(ra)
    dec=np.rad2deg(dec)
    return ra,dec


def eq2alt(jd,ra,de,lon,lat):
    '''transformacia z EQ do Azm. suradnic'''
    sid=sid_time(jd)+lon
    t=np.deg2rad(sid-ra)
    de=np.deg2rad(de)
    fi=np.deg2rad(lat)
    alt=np.arcsin(np.sin(de)*np.sin(fi)+np.cos(de)*np.cos(fi)*np.cos(t))
    alt=np.rad2deg(alt)
    return alt

def riseSet(jd,lon,lat,sun=True):
    '''calculate time of rising, transit and setting; jd - at Oh UT'''

    def rise0(dec,lat):
        dec=np.deg2rad(dec)
        lat=np.deg2rad(lat)

        ha=np.arccos(-np.tan(lat)*np.tan(dec))
        ha=np.rad2deg(ha)
        return ha

    def getTime(jd,x):
        tmp=jd+x/24.
        tmp=jd2date(tmp)
        return tmp.hour+tmp.minute/60.+tmp.second/3600.

    if sun: coord=sunCoordinates
    else: coord=moonCoordinates

    ra,dec=coord(jd)

    sid=sid_time(jd)+lon    #local sidereal time
    ha=rise0(dec,lat)
    t=(ra-sid)/15.  #transit
    if np.isnan(ha): return 'NA',t,'NA'    #nie je vychod/zapad
    r=t-ha/15.           #rise
    s=t+ha/15.           #set

    if sun: coord=sunCoordinates
    else: coord=moonCoordinates

    #corrections (moving object)
    ra,dec=coord(jd+t/24.)
    t=(ra-sid)/15.   #transit
    ra,dec=coord(jd+r/24.)
    ha=rise0(dec,lat)
    r=(ra-sid-ha)/15.           #rise
    ra,dec=coord(jd+s/24.)
    ha=rise0(dec,lat)
    s=(ra-sid+ha)/15.           #rise

    r=getTime(jd,r)
    t=getTime(jd,t)
    s=getTime(jd,s)

    return r,t,s



def moonDist(jd,ra,dec):
    raM,decM=moonCoordinates(jd)

    raM=np.deg2rad(raM)
    decM=np.deg2rad(decM)
    ra=np.deg2rad(ra)
    dec=np.deg2rad(dec)

    d=np.rad2deg(np.arccos(np.sin(dec)*np.sin(decM)+np.cos(dec)*np.cos(decM)*np.cos(ra-raM)))
    return d

def phase(jd):
    date=jd2date(jd)
    k=round((date.year+date.month/12.+date.day/365.-2000)*12.3685)
    T=k/1236.85
    newm=2451550.09766+29.530588861*k+0.00015437*T**2-0.000000150*T**3+0.00000000073*T**4  #predosli nov
    while jd<newm: newm-=29.530588861
    age=jd-newm
    phase=age/29.530588861
    return phase

