import objects as objClass
import stars 

class siteClass():
    def __init__(self,name,lat,lon,ele,limits=None):
        self.name=name
        self.lat=lat
        self.lon=lon
        self.ele=ele
        if limits is None: self.limits=[0,90,0,360]     #min_alt,max_alt,min_az,max_az
        else: self.limits=limits

constellations=stars.load()

f1='data/objects-moje.opd'
objects1=objClass.objects(constellations)
objects1.load(f1)

f2='data/objects-planner.opd'
objects2=objClass.objects(constellations)
objects2.load(f2)

for obj in objects2.objects:
    if obj in objects1.objects:
        print(obj)
        break
    objects1.objects[obj]=objects2.objects[obj]
    
objects1.save(f1)
