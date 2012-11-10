from django.db import models
from django.dispatch.dispatcher import receiver

# Create your models here.


class Student(models.Model):
    sep_id = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dec = models.BooleanField(default=False)
    parents_name = models.CharField(max_length=60)
    parents_email = models.EmailField(max_length=254)
    grade = models.IntegerField()
    phone = models.CharField(max_length=20)
    r_score_in = models.CharField(max_length=6,blank=True,null=True)
    w_score_in = models.CharField(max_length=6,blank=True,null=True)
    r_score_out = models.CharField(max_length=6,blank=True,null=True)    
    w_score_out = models.CharField(max_length=6,blank=True,null=True)
    notes = models.TextField(blank=True,null=True)

class Klass(models.Model):
    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    name = models.CharField(max_length=20)
    active = models.BooleanField(default=False)
    date = models.DateField()   

    students = models.ManyToManyField('Student', related_name="klasses", through='Interaction',blank=True,null=True)

class Interaction(models.Model):
    q1 = models.BooleanField(default=False)
    q2 = models.BooleanField(default=False)
    teacher  = models.CharField(max_length=10)
    status = models.CharField(max_length=10)

    student = models.ForeignKey('Student')
    klass = models.ForeignKey('Klass')    

    records = models.ManyToManyField("Record", related_name="interactions")

@receiver(models.signals.pre_delete, sender=Interaction)
def _delete_interaction(sender,instance,**kwargs): 
    for r in instance.records.all(): 
        if r.interactions.count() == 1: 
            r.delete()


class Record(models.Model): 
    timestamp = models.DateTimeField(auto_now=True)
    notes = models.TextField()

