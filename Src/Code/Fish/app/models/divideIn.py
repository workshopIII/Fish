from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base

class DivideIn(Base):
    __tablename__ = 'divideIn'
    did = Column(Integer, primary_key=True, nullable=False)
    CourseId = Column(String(50), nullable=False)
    staffID = Column(String(50),nullable=False)
    methodNo = Column(Integer,  nullable=False)
    numberPergroup = Column(Integer)
    totalStu = Column(Integer)
    rest = Column(Integer)
    groupNNormal = Column(Integer)
    totalGroup = Column(Integer)

    def __init__(self, did,  CourseId,staffID,methodNo,numberPergroup,totalStu,rest,groupNNormal,totalGroup):
        super(DivideIn,self).__init__()
        self.did = did
        self.staffID = staffID
        self.CourseId = CourseId
        self.methodNo = methodNo
        self.numberPergroup = numberPergroup
        self.totalStu = totalStu
        self.totalGroup = totalGroup#总小组数量（包括不是预定组人数的小组数量）
        self.rest = rest#不是预定组人数的小组数量
        self.groupNNormal = groupNNormal#那些不是预定组人数的小组的人数
division = DivideIn('','','','','','','','','')