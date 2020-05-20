from sqlalchemy import Column, String, Integer, Float, orm, ForeignKey
from sqlalchemy.testing.config import db
from app.models.base import Base

class Student(Base):
    __tablename__ = 'student'
    StudentID = Column(String(50), primary_key=True)
    StuName = Column(String(30))
    GPA = Column(String(30))
    Email = Column(String(50),nullable = False)

    def __init__(self, StudentID, StuName, email, GPA):
        super(Student,self).__init__()
        self.StudentID = StudentID
        self.StuName = StuName
        self.Email = email
        self.GPA = GPA
        


    def jsonstr(self):

        jsondata = {
            'StuName':self.StuName,
            'id': self.StudentID,
            'email': self.Email,
            'GPA': self.GPA,
            
        }
        return jsondata
studentPublic = Student('','','','')
