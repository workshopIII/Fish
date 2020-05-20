from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base

class Course_student(Base):
    __tablename__ = 'Course_student'
    rrrid = Column(Integer, primary_key=True, autoincrement=True)
    studentID = Column(String(50))
    CourseId = Column(String(50), nullable=False) 
    sectionNo = Column(String(50), nullable=False) 

    def __init__(self, rrrid, studentID, CourseId,sectionNo):
        super(Course_student,self).__init__()
        self.rrrid = rrrid
        self.studentID = studentID
        self.CourseId = CourseId
        self.sectionNo = sectionNo
currentStudent = Course_student('','','','')