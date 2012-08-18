from tastypie.resources import ModelResource
from log.models import Student,Klass

from tastypie.api import Api
from tastypie.authorization import Authorization


class StudentResource(ModelResource):
    class Meta:
        queryset = Student.objects.all()
        resource_name = 'student'
        authorization= Authorization()

class KlassResource(ModelResource):
    class Meta: 
        queryset = Klass.objects.all()
        resource_name = 'class'
        authorization = Authorization()        


v1_api = Api(api_name='v1')
v1_api.register(StudentResource())
v1_api.register(KlassResource())
