from sqlalchemy import Column, Integer, String, orm
from app.models.base import Base


class Invitation(Base):
    __tablename__ = 'invitation'
    iid = Column(Integer, primary_key=True, autoincrement=True)
    CourseId = Column(String(50), nullable=False)
    sectionNo = Column(String(50), nullable=False) 
    studentID = Column(String(50))
    selection = Column(String(50))#跟studentID一样都是收的studentID
    confirm = Column(Integer)

    def __init__(self, iid,courseId, sectionNo, studentID,selection,confirm):
        super(Invitation,self).__init__()
        self.iid = iid
        self.CourseId = courseId
        self.sectionNo = sectionNo
        self.studentID = studentID
        self.selection = selection
        self.confirm = confirm