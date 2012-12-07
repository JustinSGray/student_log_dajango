from django.db import models
from django.dispatch.dispatcher import receiver

from django.contrib.auth.models import User


# Create your models here.


class Student(models.Model):
    class Meta: 
        ordering = ["last_name","first_name"]

    sep_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dec = models.BooleanField(default=False)
    parents_name = models.CharField(max_length=60)
    parents_email = models.EmailField(max_length=254,null=True,blank=True)
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

    #students = models.ManyToManyField('Student', related_name="klasses", through='Interaction',blank=True,null=True)

class Interaction(models.Model):
    class Meta: 
        ordering = ["klass__date"]

    q1 = models.BooleanField(default=False)
    q2 = models.BooleanField(default=False)
    teacher  = models.CharField(max_length=10)
    status = models.CharField(max_length=10)

    student = models.ForeignKey('Student',related_name="interactions")
    klass = models.ForeignKey('Klass',related_name="interactions")

    #records = models.ManyToManyField("Record", related_name="interactions")

@receiver(models.signals.pre_delete, sender=Interaction)
def _delete_interaction(sender,instance,**kwargs): 
    for r in instance.records.all(): 
        if r.interactions.count() <= 1: 
            r.delete()


class Record(models.Model): 
    timestamp = models.DateTimeField()
    notes = models.TextField()
    
    students = models.ManyToManyField('Student', related_name="records")

    klass = models.ForeignKey('Klass')

