from sqlalchemy import Column, String, Integer, orm ,Float
from app.models.base import Base

class Member(Base):
    __tablename__='member'
    mid =  Column(Integer, primary_key=True,autoincrement=True)
    StudentID = Column(String(50))
    CourseId = Column(String(50), nullable=False)
    sectionNo = Column(String(50), nullable=False)
    contribution = Column(Float)
    tid = Column(Integer)
    vote = Column(String(50), default = 'undefined')
    default = Column(Integer)


    def __init__(self, mid,studentID, courseId, sectionNo,contribution,tid,vote,default):
        super(Member,self).__init__()
        self.mid = mid
        self.StudentID = studentID
        self.CourseId = courseId
        self.sectionNo = sectionNo
        self.tid = tid
        self.contribution = contribution
        self.vote = vote
        self.default = default
currentMember = Member('','','','','','','','')