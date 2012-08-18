from django.db import models

# Create your models here.


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dec = models.BooleanField(default=False)
    parent_name = models.CharField(max_length=60)
    parent_email = models.EmailField(max_length=254)
    DOB = models.DateField()
    grade = models.IntegerField()
    phone_number = models.CharField(max_length=20)
    r_score_in = models.IntegerField(blank=True,null=True)
    w_score_in = models.IntegerField(blank=True,null=True)
    r_score_out = models.IntegerField(blank=True,null=True)    
    w_score_out = models.IntegerField(blank=True,null=True)
    notes = models.TextField(blank=True,null=True)

class Klass(models.Model):
    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    name = models.CharField(max_length=20)
    active = models.BooleanField(default=False)
    date = models.DateField()   

    students = models.ManyToManyField('Student', related_name="classes",blank=True,null=True)

class Proctor(models.Model):
    q1 = models.BooleanField(default=False)
    q2 = models.BooleanField(default=False)

    student = models.ForeignKey('Student')
    klass = models.ForeignKey('Klass')     

class Record(models.Model): 
    timestamp = models.DateTimeField(auto_now=True)
    notes = models.TextField()

    student = models.ForeignKey('Student')
    klass = models.ForeignKey('Klass') 