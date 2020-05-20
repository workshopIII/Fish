from flask import Blueprint,render_template, request
from app.models.course_student import Course_student

course_studentBP = Blueprint('course_student',__name__)

@course_studentBP.route('', methods=['GET'])
def get_course_student():
    with Course_student.auto_commit():
        course_student = Course_student("Mario", 3.0,'aaa@mail.uic.edu.hk','A','123456')
        # 数据库的insert操作
        Course_student.session.add(course_student)
    
    return 'hello Class1'