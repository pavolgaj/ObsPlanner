class observation:
    def __init__(self,obj,date,obs,tel,site,image='',note=''):
        self.obj=obj
        self.date=date
        self.jd=0
        self.observer=obs
        self.telescope=tel
        self.site=site
        self.image=image
        self.note=note
