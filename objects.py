import numpy as np
import stars
import os
import pickle 
from observation import *

class objects:    
    def __init__(self,constellations):
        self.objects={}
        self.constellations=constellations
        
    def load(self,name):
        f=open(name,'rb')
        self.objects=pickle.load(f)
        f.close()
    
    def add(self,name,ra,dec,mag,size='',typ='',note='',const=''):
        '''add object'''
        obj=stars.star(name,ra,dec,mag,size,typ,note,const)           
        self.objects[name]={'object':obj,'obs':{}}

    def addObs(self,obj,date,observer,telescope,site,image='',note=''):
        '''add observation of object'''
        obs=observation(obj,date,observer,telescope,site,image,note)
        self.objects[obj]['obs'][obs.date]=obs

    def save(self,name):
        f=open(name,'wb')
        pickle.dump(self.objects,f)
        f.close()
