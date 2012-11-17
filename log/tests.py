from django.utils import unittest

from django.test.client import Client

from tastypie.test import ResourceTestCase

from log.models import Klass,Student,Interaction,Record

class RecordTest(ResourceTestCase):
    fixtures = ["test_data.json",]

    def setUp(self):
        super(RecordTest,self).setUp()
        self.q = "/api/v1/records/"
        self.detail_url = self.q+"1/"

    def test_get(self): 
        resp = self.api_client.get(self.q, format="json")
        self.assertValidJSONResponse(resp)

        data = self.deserialize(resp)

        self.assertEqual(data['meta']['total_count'],2)

    def test_post(self): 
        resp = self.api_client.post(self.q,data={
            "notes":True,
            "timestamp":"2012-11-01",
            "interactions":['/api/v1/interactions/1/',
                            '/api/v1/interactions/2/']
            })

        self.assertHttpCreated(resp)
        self.assertEqual(Record.objects.count(),3)

        resp = self.api_client.get("/api/v1/interactions/2/",format="json")
        data = self.deserialize(resp)

        self.assertEqual(len(data['records']),3)

        resp = self.api_client.get("/api/v1/interactions/1/",format="json")
        data = self.deserialize(resp)

        self.assertEqual(len(data['records']),1)



class ClassTest(ResourceTestCase):
    fixtures = ["test_data.json",]

    def setUp(self): 
        super(ClassTest,self).setUp()
        self.q = "/api/v1/classes/"
        self.detail_url = self.q +"1/"
    
    def test_get(self):
        resp = self.api_client.get(self.q, format="json")
        self.assertValidJSONResponse(resp)

        data = self.deserialize(resp)

        self.assertEqual(data['meta']['total_count'],3)

        self.assertEqual(set(data['objects'][0].keys()),
            set(["active","id","name","date","resource_uri","interactions"]))

        resp = self.api_client.get(self.detail_url, format="json")
        data = self.deserialize(resp)
        
        self.assertEqual(len(data['interactions']),3)

    def test_post(self):
        resp = self.api_client.post(self.q,data={
            "active":True,
            "name":"Test Class",
            "date":"2011-05-22",
            })

        self.assertHttpCreated(resp)
        self.assertEqual(Klass.objects.count(),4)

    def test_put(self):
        resp = self.api_client.get(self.detail_url, format="json")
        orig_data = self.deserialize(resp)
   
        new_data = orig_data.copy()
        new_data['active'] = False

        resp = self.api_client.put(self.detail_url,data=new_data,format="json")
        self.assertHttpAccepted(resp)
        self.assertEqual(Klass.objects.count(),3)  #shoudl not have changed


    def test_delete(self):
        self.assertEqual(Klass.objects.count(),3)
        resp = self.api_client.delete(self.detail_url,format="json")
        self.assertEqual(Klass.objects.count(),2)
        self.assertEqual(Student.objects.count(),3) #don't remove students
        self.assertEqual(Interaction.objects.count(),0) #cascade to the interactions
        self.assertEqual(Record.objects.count(),0) #cascade any orphan records


class InteractionTest(ResourceTestCase):         
    fixtures = ["test_data.json",]

    def setUp(self): 
        super(InteractionTest,self).setUp()
        self.set_url = "/api/v1/interactions/"
        self.detail_url = self.set_url+"2/"

    def test_get(self): 
        
        resp = self.api_client.get(self.set_url, format="json")
        data = self.deserialize(resp)

        self.assertValidJSONResponse(resp)

        self.assertEqual(data['meta']['total_count'],3)

        resp = self.api_client.get(self.detail_url, format="json")
        data = self.deserialize(resp)

        self.assertValidJSONResponse(resp)
        
        keys = data.keys()
        for name in ['status','teacher','q1','q2','records']: 
            self.assertIn(name,keys)

        self.assertEqual(len(data['records']),2)


    def test_put(self):
        resp = self.api_client.get(self.detail_url, format="json")
        orig_data = self.deserialize(resp)
   
        new_data = orig_data.copy()
        new_data['q1'] = False
        new_data['send_msg'] = True

        #print new_data

        #self.assertEqual(set(new_data.keys()),set(other_data.keys()))

        resp = self.api_client.put(self.detail_url,
            data=new_data,format="json")
        self.assertHttpAccepted(resp)

    def test_post(self):
        pass 

    def test_delete(self): 
        
        self.assertEqual(Klass.objects.count(),3)
        self.assertEqual(Student.objects.count(),3)
        self.assertEqual(Interaction.objects.count(),3)
        self.assertEqual(Record.objects.count(),2)
        
        self.api_client.delete(self.detail_url,format="json")

        self.assertEqual(Klass.objects.count(),3)
        self.assertEqual(Student.objects.count(),3)
        self.assertEqual(Interaction.objects.count(),2)
        self.assertEqual(Record.objects.count(),0)





