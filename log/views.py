import StringIO

from django.http import HttpResponse,Http404

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.api import Api
from tastypie.authorization import Authorization

from log.models import Student,Klass,Record,Interaction
from log.roster_parser import parse_roster


def load_roster(request,classId):
    if request.method == 'POST':
        f = StringIO.StringIO(request.FILES['file'].read())
        students = parse_roster(f)
        klass = Klass.objects.get(pk=classId)
        for row in students: 

            try: 
                student = Student.objects.get(pk=row['sep_id'])
            except Student.DoesNotExist: 
                data = row.copy()
                del data['status'] #status is for interaction model
                student = Student(**data)
                student.save()
            try:
                Interaction.objects.get(klass=klass,student=student)
            except Interaction.DoesNotExist:     
                inter = Interaction(klass=klass,student=student,
                    status=row['status'],teacher='GenEd')
                inter.save()

        return HttpResponse(status=201)
    
    raise Http404

class SmallKlassResource(ModelResource):
    class Meta: 
        queryset = Klass.objects.select_related().all()
        resource_name = 'classes'
        authorization = Authorization() 
        always_return_data = True
    date = fields.DateField(attribute="date")

#have to do this janky thing to avoid recursion in the Interaction resource, because of through model
class KlassResource(SmallKlassResource): 

    interactions =  fields.ToManyField("log.views.SmallInteractionsResource",
        attribute= 'interactions',
        full=True,
        blank=True,null=True)
    
    #block the definition of students during put and post
    def save_m2m(self,bundle): 
        pass


class SmallStudentsResource(ModelResource): 
    class Meta: 
        queryset = Student.objects.select_related().all()
        resource_name = "students"
        authorization = Authorization()

class StudentsResource(SmallStudentsResource): 

    records = fields.ToManyField("log.views.RecordsResource","records",full=True)


class RecordsResource(ModelResource):
    class Meta: 
        queryset = Record.objects.select_related('klass').all()
        resource_name = "records"
        authorization = Authorization() 
    
    timestamp = fields.DateTimeField(attribute="timestamp")
    klass = fields.ToOneField("log.views.SmallKlassResource","klass",full=True)
    students = fields.ToManyField("log.views.StudentsResource","students")

class SmallInteractionsResource(ModelResource): 
    class Meta:
        queryset = Interaction.objects.all()
        resource_name = 'interactions'
        authorization= Authorization()

    status = fields.CharField(attribute="status",null=True)
    teacher = fields.CharField(attribute="teacher",null=True)
    q1 = fields.BooleanField(attribute="q1",null=True)
    q2 = fields.BooleanField(attribute="q2",null=True)

    student =  fields.ToOneField("log.views.SmallStudentsResource","student",full=True) 

    
class InteractionsResource(ModelResource):
    class Meta:
        queryset = Interaction.objects.select_related().all()
        resource_name = 'interactions'
        authorization= Authorization()

    status = fields.CharField(attribute="status",null=True)
    teacher = fields.CharField(attribute="teacher",null=True)
    q1 = fields.BooleanField(attribute="q1",null=True)
    q2 = fields.BooleanField(attribute="q2",null=True)

    student =  fields.ToOneField("log.views.StudentsResource","student",full=True) 

    klass   =  fields.ToOneField("log.views.SmallKlassResource",'klass',full=True)
    #records = fields.ToManyField("log.views.RecordsResource",
    #    attribute = lambda bundle: Record.objects.filter(interactions__student=bundle.obj.student),
    #    full=True)

    def save_m2m(self,bundle): 
        pass


v1_api = Api(api_name='v1')
v1_api.register(KlassResource())
v1_api.register(InteractionsResource())
v1_api.register(StudentsResource())
v1_api.register(RecordsResource())
