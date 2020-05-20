from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base


class CourseTeamStudent(Base):
    __tablename__ = 'CourseTeamStudent'
    rid = Column(Integer, primary_key=True)
    CourseId = Column(String(50), nullable=False)
    Tid = Column(Integer)
    StudentID = Column(String(50))
    sectionNo = Column(String(50), nullable=False) 


    def __init__(self, rid, CourseId, Tid, StudentID,sectionNo):
        super(CourseTeamStudent,self).__init__()
        self.rid = rid
        self.CourseId = CourseId
        self.Tid = Tid
        self.StudentID = StudentID
        self.sectionNo = sectionNo