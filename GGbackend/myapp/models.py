from django.db import models

class MachinePyro(models.Model):
    addpyro = models.IntegerField(default=0)  # Total pyro value
    pyro = models.IntegerField() 
    machineid = models.CharField(max_length=50)
    received = models.CharField(max_length=50, blank=True, null=True)
    processing = models.CharField(max_length=50, blank=True, null=True)
    dispatched = models.CharField(max_length=50, blank=True, null=True)
    pro=models.IntegerField()
    con=models.IntegerField()
   

    


    def __str__(self):
        return f'addpyro-{self.addpyro}, machineid-{self.machineid},  pyro-{self.pyro} received-{self.received} ,processing-{self.processing}  , dispatched-{self.dispatched} , con-{self.con} , pro-{self.pro}'


class MachineBsfl(models.Model):
    addbsfl = models.IntegerField(default=0)  
    bsfl = models.IntegerField()  
    machineid = models.CharField(max_length=50)
    bsreceived = models.CharField(max_length=50, blank=True, null=True)
    composting = models.CharField(max_length=50, blank=True, null=True)
    manure = models.CharField(max_length=50, blank=True, null=True)
    com=models.IntegerField()
    man=models.IntegerField()
    
    

    def __str__(self):
        return f'addbsfl-{self.addbsfl} ,machineid-{self.machineid} ,bsfl-{self.bsfl} ,received-{self.bsreceived} ,composting-{self.composting},manure- {self.manure} ,com-{self.com} ,man-{self.man} '


class Admingreen(models.Model):
    machineid=models.CharField(max_length=100)
    adname=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    
    def __str__(self):
        return f'machineid-{self.machineid},username-{self.adname},password-{self.password}'
class Usergreen(models.Model):
    machineid=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    Bsmachineid=models.CharField(max_length=100)
    pyroweigh=models.IntegerField()
    bsflweight=models.IntegerField()
    addpyroweight=models.IntegerField()
    addbsflweight=models.IntegerField()
    carbon=models.IntegerField()
    def __str__(self):
        return f'machineid-{self.machineid},Bsmachineid-{self.Bsmachineid},username-{self.username},password-{self.password},pyroweight-{self.pyroweigh},bsflweight-{self.bsflweight},addpyroweight-{self.addpyroweight},addbsflweight-{self.addbsflweight},carbon-{self.carbon}'
