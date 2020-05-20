from flask import Blueprint,render_template, request
from app.models.course_teacher import Course_teacher

course_teacherBP = Blueprint('course_teacher',__name__)

@course_teacherBP.route('', methods=['GET'])
def get_course_teacher():
    with Course_teacher.auto_commit():
        course_teacher = Course_teacher("Mario", 3.0,'aaa@mail.uic.edu.hk','A','123456')
        # 数据库的insert操作
        Course_teacher.session.add(course_teacher)
    
    return 'hello Class1'