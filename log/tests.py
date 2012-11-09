from django.utils import unittest

from django.test.client import Client

from tastypie.test import ResourceTestCase


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

        print self.q+"1/"
        resp = self.api_client.get(self.q+"1/", format="json")
        data = self.deserialize(resp)
        
        self.assertEqual(data,{
            "active":True,
            "id":"1",
            "name":"Class 1",
            "date":"2012-11-01",
            "resource_uri":"/api/v1/classes/1/",
            "students":['api/v1/students/1',
            'api/v1/students/2',]
            })

    def test_post(self):
        pass

    def test_put(self):
        pass
        
    def test_delete(self):
        pass        

