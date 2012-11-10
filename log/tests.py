from django.utils import unittest

from django.test.client import Client

from tastypie.test import ResourceTestCase

from log.models import Klass


class ClassTest(ResourceTestCase):
    fixtures = ["test_data.json",]

    def setUp(self): 
        super(ClassTest,self).setUp()
        self.q = "/api/v1/classes/"
    
    def test_get(self):
        resp = self.api_client.get(self.q, format="json")
        self.assertValidJSONResponse(resp)

        data = self.deserialize(resp)

        self.assertEqual(data['meta']['total_count'],3)

        self.assertEqual(set(data['objects'][0].keys()),
            set(["active","id","name","date","resource_uri","students"]))

        print self.q+"1/"
        resp = self.api_client.get(self.q+"1/", format="json")
        data = self.deserialize(resp)
        
        self.assertEqual(set(data.keys()),set([
            "active",
            "id",
            "name",
            "date",
            "resource_uri",
            "students",
            ]))

    def test_post(self):
        resp = self.api_client.post(self.q,data={
            "active":True,
            "name":"Test Class",
            "date":"2011-05-22",
            })

        self.assertHttpCreated(resp)
        self.assertEqual(Klass.objects.count(),4)


    def test_put(self):
        pass
        
    def test_delete(self):
        pass        

