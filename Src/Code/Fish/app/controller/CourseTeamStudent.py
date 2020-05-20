from flask import Blueprint,render_template, request
from app.models.CourseTeamStudent import CourseTeamStudent

CourseTeamStudentBP = Blueprint('CourseTeamStudent',__name__)

@CourseTeamStudentBP.route('', methods=['GET'])
def get_CourseTeamStudent():
    with CourseTeamStudent.auto_commit():
        cts = CourseTeamStudent("ACHN0763", 1,'1730026000' )
        # 数据库的insert操作
        CourseTeamStudent.session.add(cts)
    
    return 'hello member'