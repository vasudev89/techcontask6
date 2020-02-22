#!/usr/bin/env python
# coding: utf-8

# In[1]:


from abc import ABC,abstractmethod
from tabulate import tabulate
import pymysql 


# In[2]:


host = "localhost"
user = "root"
password = "password@123"
dbname = "TECHCON"
port = 3306


# In[3]:


class Course:

    def __init__(self,id=None,name=None):
        self.id = id
        self.name = name

    def __str__(self):
        return "Course[name={},id={}]".format(self.name,self.id)

class CourseDAO(ABC):
  @abstractmethod
  def add(self, name):pass
  @abstractmethod
  def fetch(self, id=None):pass

class CourseDAOImpl(CourseDAO):
    def add(self, name):
        try:
            if not name: return False
            query = "INSERT INTO COURSES (NAME) VALUES ('%s')"%name
            with pymysql.connect(host = host,user = user,password = password,db = dbname,port = port) as cur:
                cur.execute(query)
                return True
        except Exception as e:
            print(e) 
            return False

    def fetch(self, id=None):
        try:
            query = "SELECT * FROM COURSES" if not id else "SELECT * FROM COURSES WHERE ID=%s"%id
            with pymysql.connect(host = host,user = user,password = password,db = dbname,port = port,cursorclass=pymysql.cursors.DictCursor) as cur:
                cur.execute(query)
                res = cur.fetchall()
                if not res: return False
                else: return res
                
                return True
        except Exception as e:
            print(e) 
            return False


# In[4]:


class StudentDAO(ABC):
  @abstractmethod
  def add(self, name,courseid):pass
  @abstractmethod
  def fetch(self):pass
  @abstractmethod
  def updatestudent(self,id,status):pass

class StudentDAOImpl(StudentDAO):
    def add(self, name,courseid):
        try:
            if not name: return False
            query = "INSERT INTO STUDENTS (NAME,COURSEID) VALUES ('%s',%s)"%(name,courseid)
            with pymysql.connect(host = host,user = user,password = password,db = dbname,port = port) as cur:
                cur.execute(query)
            return True
        except Exception as e:
            print(e) 
            return False

    def fetch(self):
        try:
            query = "SELECT * FROM STUDENTS JOIN COURSES ON STUDENTS.COURSEID = COURSES.ID"
            with pymysql.connect(host = host,user = user,password = password,db = dbname,port = port,cursorclass=pymysql.cursors.DictCursor) as cur:
                cur.execute(query)
                res = cur.fetchall()
                if not res: return False
                else: return res
                return True
        except Exception as e:
            print(e) 
            return False
        
    def updatestudent(self,id,status):
        try:
            query = "UPDATE STUDENTS SET STATUS = '%s' WHERE ID = %s"%(status, id)
            print(query)
            with pymysql.connect(host = host,user = user,password = password,db = dbname,port = port,cursorclass=pymysql.cursors.DictCursor) as cur:
                cur.execute(query)
                return True
        except Exception as e:
            print(e) 
            return False


# In[5]:


while True:
    print("0. EXIT")
    print("1. ADD COURSE")
    print("2. VIEW COURSES")
    print("3. ADD STUDENT")
    print("4. VIEW STUDENTS")
    print("5. UPDATE STUDENT STATUS")
    ch = int(input("ENTER CHOICE:"))

    if ch == 0: break
    elif ch == 1: CourseDAOImpl().add(input("ENTER COURSE NAME:"))
    elif ch == 2: 
        id = input("ENTER ID(BLANK FOR VIEWING ALL):")
        if not id:
            res = CourseDAOImpl().fetch()
            if not res: print("NO DATA")
            else:
                print( tabulate(res, headers="keys",tablefmt="psql") )
    elif ch == 3: StudentDAOImpl().add(input("ENTER STUDENT NAME:"),int( input("ENTER COURSE ID:") ))
    elif ch == 4:
        res = StudentDAOImpl().fetch()
        if not res: print("NO DATA")
        else:
            print( tabulate(res, headers="keys",tablefmt="psql") )
    elif ch == 5:
        id = int(input("ENTER STUDENT ID:"))
        status = input("ENTER STUDENT STATUS(CHOOSE FROM ('PASS','FAIL','UNMARKED'))")
        if status not in ('PASS','FAIL','UNMARKED'): print("INVALID CHOICE!!")
        else:
            StudentDAOImpl().updatestudent(id,status)
    else:
        print("INVALID CHOICE!!")

