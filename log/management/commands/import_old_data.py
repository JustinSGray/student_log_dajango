import sqlite3

from django.core.management.base import BaseCommand, CommandError

from log.models import Klass, Student, Interaction, Record

class Command(BaseCommand):

    def handle(self, *args, **option):

        conn = sqlite3.connect(args[0])
        c = conn.cursor()
        
        q = """SELECT student_id, 
                      first_name, 
                      last_name ,
                      dec, 
                      parent_name, 
                      parent_email, 
                      grade, 
                      phone_number, 
                      r_score_in, 
                      w_score_in, 
                      r_score_out, 
                      w_score_out, 
                      notes 
                      from STUDENTS"""

        keys = ('sep_id', 
              'first_name', 
              'last_name' ,
              'dec', 
              'parents_name', 
              'parents_email', 
              'grade', 
              'phone', 
              'r_score_in', 
              'w_score_in', 
              'r_score_out', 
              'w_score_out', 
              'notes' )
        
        students = {}
        for old_s in c.execute(q): 
            data = dict(zip(keys,old_s))
             
            if old_s[0] < 100 or old_s[1]=='': #crappy data hanging around
                continue 
            
            new_s = Student()
            for k in keys: 
                setattr(new_s,k,data[k])
            try:     
                new_s.save()
            except: 
                print old_s    
            students[old_s[0]] = new_s
        
        q = """SELECT  class_id, name, active,
                       date 
                       from CLASSES"""    
        
        keys = ('pk','name','active','date')

        klasses = {}
        for old_c in c.execute(q): 
            data = dict(zip(keys,old_c))
            print old_c
            new_c = Klass()
            for k in keys: 
                setattr(new_c,k,data[k])
            new_c.save()   
            klasses[data['pk']] = new_c         
        
        q = """ SELECT PROCTOR.q1,
                       PROCTOR.q2,
                       CLASSES_STUDENTS.status,
                       CLASSES_STUDENTS.teach_assn,
                       PROCTOR.student_id,
                       PROCTOR.class_id 
                from PROCTOR INNER JOIN CLASSES_STUDENTS ON 
                CLASSES_STUDENTS.student_id=PROCTOR.student_id AND
                CLASSES_STUDENTS.class_id=PROCTOR.class_id"""

        for old_p in c.execute(q): 
            new_i = Interaction()
            new_i.q1 = old_p[0]
            new_i.q2 = old_p[1]
            new_i.status = old_p[2]
            new_i.teacher = old_p[3]
            
            try: 
                new_i.student = students[old_p[4]]
                new_i.klass = klasses[old_p[5]]
            except KeyError: 
                continue #just some bad data    
            
            try: 
                new_i.save()
            except: 
                print old_p    
        
        q = """SELECT datetime, 
                      notes, 
                      student_id,
                      class_id   
                FROM RECORDS""" 

        for old_r in c.execute(q): 
            new_r = Record()
            new_r.timestamp = old_r[0]+"-05:00"
            new_r.notes = old_r[1]
            new_r.klass = klasses[old_r[3]]

            new_r.save()

            new_r.students.add(students[old_r[2]])
            new_r.save()
