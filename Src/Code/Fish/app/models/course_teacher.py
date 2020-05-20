from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base

class Course_teacher(Base):
    __tablename__ = 'course_teacher'
    rrid = Column(Integer, primary_key=True, autoincrement=True)
    staffID = Column(String(50))
    CourseId = Column(String(50), nullable=False) 
    sectionNo = Column(String(50), nullable=False) 

    def __init__(self, rrid, staffID, CourseId,sectionNo ):
        super(Course_teacher,self).__init__()
        self.rrid = rrid
        self.staffID = staffID
        self.CourseId = CourseId
        self.sectionNo = sectionNo
currentCourse = Course_teacher('','','','')