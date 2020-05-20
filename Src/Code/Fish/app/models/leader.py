from sqlalchemy import Column, String, Integer, orm, Float
from app.models.base import Base


class Leader(Base):
    __tablename__ = 'leader'
    lid = Column(Integer, primary_key=True,autoincrement=True)
    StudentID = Column(String(50), primary_key=True)
    CourseId = Column(String(50),  nullable=False)
    sectionNo = Column(String(50), nullable=False)
    Tid = Column(Integer)
    contribution = Column(Float)
    bonus = Column(Float)
    default = Column(Integer)

    def __init__(self, lid,studentID, CourseId,sectionNo, Tid,contribution,bonus,default):
        super(Leader,self).__init__()
        self.lid = lid
        self.StudentID = studentID
        self.CourseId = CourseId
        self.sectionNo = sectionNo
        self.Tid = Tid
        self.contribution = contribution
        self.bonus = bonus
        self.default =default
