import datetime
from stars import juldat

class observation:
    def __init__(self,obj,dt,obs,tel,site,image='',note=''):
        self.obj=obj
        self.date=dt.strftime('%Y-%m-%d %H:%M:%S')
        self.datetimeObject=dt
        self.jd=juldat(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second)
        self.observer=obs
        self.telescope=tel
        self.site=site
        self.image=image
        self.note=note
