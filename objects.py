import numpy as np
import stars
import os
import pickle 
from observation import *

class objects:
    #global constellations
    
    def __init__(self,constellations):
        if os.path.isfile('data/objects.opd'):
            f=open('data/objects.opd','rb')
            self.objects=pickle.load(f)
            f.close()
        else: self.objects={}
        self.constellations=constellations
        #return self.objects  
    
    def add(self,name,ra,dec,mag,size='',typ='',note='',const=''):
        obj=stars.star(name,ra,dec,mag,size,typ,note,const)           
        self.objects[name]={'object':obj,'obs':{}}

    def addObs(self,obj,date,observer,telescope,site,image='',note=''):
        obs=observation(obj,date,observer,telescope,site,image,note)
        self.objects[obj]['obs'][date]=obs

    def save(self):
        f=open('data/objects.opd','wb')
        pickle.dump(self.objects,f)
        f.close()
