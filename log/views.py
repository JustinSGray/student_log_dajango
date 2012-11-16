from tastypie.resources import ModelResource
from log.models import Student,Klass,Record,Interaction

from tastypie import fields
from tastypie.api import Api
from tastypie.authorization import Authorization


class SmallKlassResource(ModelResource):
    class Meta: 
        queryset = Klass.objects.all()
        resource_name = 'classes'
        authorization = Authorization() 

#have to do this janky thing to avoid recursion in the Interaction resource, because of through model
class KlassResource(SmallKlassResource): 

    interactions =  fields.ToManyField("log.views.InteractionsResource",
        attribute= lambda bundle: Interaction.objects.filter(klass=bundle.obj),
        full=True,
        blank=True,null=True)
    
    #block the definition of students during put and post
    def save_m2m(self,bundle): 
        pass



class StudentsResource(ModelResource): 
    class Meta: 
        queryset = Student.objects.all()
        resource_name = "students"
        authorization = Authorization()      

class RecordsResource(ModelResource):
    class Meta: 
        queryset = Record.objects.all()         
        resource_name = "records"
        authorization = Authorization() 

class InteractionsResource(ModelResource):
    class Meta:
        queryset = Interaction.objects.all()
        resource_name = 'interactions'
        authorization= Authorization()

    status = fields.CharField(attribute="status",null=True)
    teacher = fields.CharField(attribute="teacher",null=True)
    q1 = fields.BooleanField(attribute="q1",null=True)
    q2 = fields.BooleanField(attribute="q2",null=True)

    student =  fields.ToOneField("log.views.StudentsResource","student",full=True) 
    klass   =  fields.ToOneField("log.views.SmallKlassResource",'klass',full=True)
    records = fields.ToManyField("log.views.RecordsResource","records",full=True)


v1_api = Api(api_name='v1')
v1_api.register(KlassResource())
v1_api.register(InteractionsResource())
v1_api.register(StudentsResource())
