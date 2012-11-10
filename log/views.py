from tastypie.resources import ModelResource
from log.models import Student,Klass

from tastypie import fields
from tastypie.api import Api
from tastypie.authorization import Authorization


class StudentResource(ModelResource):
    class Meta:
        queryset = Student.objects.all()
        resource_name = 'students'
        authorization= Authorization()

    #klasses =  fields.ToManyField("log.views.KlassResource","students",full=True)
   

class KlassResource(ModelResource):
    class Meta: 
        queryset = Klass.objects.all()
        resource_name = 'classes'
        authorization = Authorization()   

    students =  fields.ToManyField("log.views.StudentResource",
        attribute="students",
        related_name="klasses",full=True,
        blank=True,null=True)
    
    #block the definition of students during put and post
    def save_m2m(self,bundle): 
        pass

v1_api = Api(api_name='v1')
v1_api.register(StudentResource())
v1_api.register(KlassResource())