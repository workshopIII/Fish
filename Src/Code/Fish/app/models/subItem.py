from sqlalchemy import Column, String, Integer, orm, Float
from app.models.base import Base

class SubItem(Base):
    __tablename__='subItem'
    Sid = Column(Integer, primary_key=True, autoincrement=True)
    sTitle = Column(String(50), nullable=False)
    percentage = Column(Float)
    CourseId = Column(String(50), nullable = False)
    sectionNo = Column(String(50), nullable=False) 

    def __init__(self, sid, sTitle, percentage, CourseId,sectionNo):
        super(SubItem,self).__init__()
        self.Sid = sid
        self.sTitle = sTitle
        self.percentage = percentage
        self.CourseId = CourseId
        self.sectionNo = sectionNo
currentSub = SubItem('','','','','')
