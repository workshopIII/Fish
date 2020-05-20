from sqlalchemy import Column, Integer, String, orm
from app.models.base import Base


class Course(Base):
    __tablename__ = 'course'
    CourseId = Column(String(50), primary_key=True, nullable=False)
    CourseName = Column(String(50), nullable=False)

    def __init__(self, courseId, courseName, stuffid):
        super(Course,self).__init__()
        self.CourseId = courseId
        self.CourseName = courseName