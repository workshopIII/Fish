from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base

class Teacher(Base):
    __tablename__ = 'teacher'
    staffid = Column(String(50), primary_key=True)
    name = Column(String(50), unique=True, nullable=True)
    email = Column(String(50), unique=True, nullable=True)

    def __init__(self, staffid, teacherName, teacherEmail):
        super(Teacher,self).__init__()
        self.staffid = staffid
        self.name = teacherName
        self.email = teacherEmail
        

    def jsonstr(self):

        jsondata = {
            'staffid': self.StaffID,
            'teacherName': self.name,
            'teacherEmail': self.email,
        }

        return jsondata
teacherPublic = Teacher('','','')