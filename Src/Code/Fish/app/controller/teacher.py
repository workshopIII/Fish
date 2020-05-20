from flask import Blueprint,render_template, request, redirect
from app.models.base import db
from app.models.teacher import Teacher
from app.models.user import User,userPublic

teacherBP = Blueprint('teacher',__name__)

@teacherBP.route('/mainPage', methods=['GET'])
def main_page():
    if request.method == 'GET' :
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print(userPublic.usertype)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')

        else:
            return render_template('teacher.html')
    else:
        pass

@teacherBP.route('/importChoice', methods=['GET'])
def import_choice():
    if request.method == 'GET':
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
        return render_template('import.html')
    else:
        pass

