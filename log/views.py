import StringIO
import json 

from django.http import HttpResponse,Http404
from django.conf.urls.defaults import url
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.api import Api
from tastypie.authorization import Authorization
from tastypie.utils import trailing_slash

from log.models import Student,Klass,Record,Interaction
from log.roster_parser import parse_roster

#@csrf_exempt
def load_roster(request,classId):
    if request.method == 'POST':
        f = StringIO.StringIO(request.FILES['file'].read())
        try: 
            students = parse_roster(f)
        except KeyError as err: 
            err_msg = 'The csv file did not have a "%s" column.'%str(err.args[0])

            return HttpResponse(content=json.dumps({'msg':err_msg}), 
                                mimetype="application/json",
                                status=415)

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

        msg = "Roster Uploaded Successfully"
        return HttpResponse(content=json.dumps({'msg':msg}),
                            mimetype="/application/json",
                            status=201)
    
    raise Http404

class SmallKlassResource(ModelResource):
    class Meta: 
        queryset = Klass.objects.all()
        resource_name = 'classes'
        authorization = Authorization() 
        always_return_data = True
    date = fields.DateField(attribute="date")

    def save_m2m(self,bundle): 
        pass

#have to do this janky thing to avoid recursion in the Interaction resource, because of through model
class KlassResource(ModelResource): 

    class Meta: 
        queryset = Klass.objects.select_related().all()
        resource_name = "classes_with_interactions"
        authorization = Authorization() 
        always_return_data = True
    
    date = fields.DateField(attribute="date")
    interactions =  fields.ToManyField("log.views.MediumInteractionsResource",
        attribute= 'interactions',
        full=True,
        blank=True,null=True)



class SmallStudentsResource(ModelResource): 
    class Meta: 
        queryset = Student.objects.select_related().all()
        resource_name = "students"
        authorization = Authorization()

    records = fields.ToManyField("log.views.RecordsResource","records",full=False,null=True,blank=True)
    

class StudentsResource(SmallStudentsResource): 

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])    
        
        q = request.GET.get('q','')

        students = Student.objects.select_related('interactions__klass').filter(Q(first_name__contains=q)|
        Q(last_name__contains=q)|
        Q(phone__contains=q)|
        Q(notes__contains=q)|
        Q(records__notes__contains=q)).annotate()

        objects = []
        if students: 
            for s in students:
                bundle = self.build_bundle(obj=s, request=request)
                bundle = self.full_dehydrate(bundle)
                objects.append(bundle)

            object_list = {
                'objects': objects,
            }
            return self.create_response(request, object_list)
        else: 
            raise Http404("Sorry, no results on that page.")

    records = fields.ToManyField("log.views.RecordsResource","records",full=True,null=True,blank=True)
    interactions = fields.ToManyField("log.views.SmallInteractionsResource","interactions",full=True,null=True,blank=True)


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
        queryset = Interaction.objects.select_related().all()
        resource_name = 'interactions'
        authorization= Authorization()
    student =  fields.ToOneField("log.views.SmallStudentsResource","student",full=False)
    klass   =  fields.ToOneField("log.views.SmallKlassResource",'klass',full=True)


class MediumInteractionsResource(ModelResource):
    class Meta:
        queryset = Interaction.objects.select_related().all()
        resource_name = 'interactions'
        authorization= Authorization()
    student =  fields.ToOneField("log.views.SmallStudentsResource","student",full=True,null=True,blank=True)
    klass   =  fields.ToOneField("log.views.SmallKlassResource",'klass',full=True,null=True,blank=True)    


    
class InteractionsResource(SmallInteractionsResource):
    status = fields.CharField(attribute="status",null=True)
    teacher = fields.CharField(attribute="teacher",null=True)
    q1 = fields.BooleanField(attribute="q1",null=True)
    q2 = fields.BooleanField(attribute="q2",null=True)

    student =  fields.ToOneField("log.views.StudentsResource","student",full=True) 
    klass   =  fields.ToOneField("log.views.SmallKlassResource",'klass',full=True)



v1_api = Api(api_name='v1')
v1_api.register(SmallKlassResource())
v1_api.register(KlassResource())
v1_api.register(MediumInteractionsResource())
v1_api.register(StudentsResource())
v1_api.register(RecordsResource())
