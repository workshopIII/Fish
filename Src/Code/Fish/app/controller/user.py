from flask import Blueprint,render_template, request, jsonify, redirect
from app.models.base import db
from app.models.user import User
import json
import urllib
import psutil
from app.models.student import Student,studentPublic
from app.models.teacher import Teacher,teacherPublic
from sqlalchemy import or_,and_,all_,any_
from flask.helpers import url_for
from app.models.user import userPublic

userBP = Blueprint('user',__name__)

@userBP.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        message = 'Please first login'
        return render_template('login.html',message = message)
    else:

        email = request.form.get('form-username')
        _password = request.form.get('form-password')
        usertype = request.form['role']
        
        
        result = User.query.filter(and_(User.username == email,User.usertype == usertype)).first() 
        
        
        
        if result:
            passw = result.psw
            if passw==_password:
                userPublic.usertype = usertype
                userPublic.username = email
                userPublic.password = _password
                if usertype == 'student':
                    studentPublic.Email = email
                    result = Student.query.filter(Student.Email==email).first()
                    studentPublic.GPA = result.GPA
                    studentPublic.StuName = result.StuName
                    studentPublic.StudentID = result.StudentID
                    return redirect('http://127.0.0.1:5000/student/mainPage')#把user传过去
                    #return render_template('http://127.0.0.1:5000/student', username = email)
                elif usertype == 'teacher':
                    teacherPublic.email = email
                    result = Teacher.query.filter(Teacher.email==email).first()
                    teacherPublic.name = result.name
                    teacherPublic.staffid = result.staffid
                    return redirect('http://127.0.0.1:5000/teacher/mainPage')
                else:
                    message = 'usertype cannot be empty'  
                    return render_template('login.html',message = message) 
            else:
                message = 'invalid password'
                return render_template('login.html',message = message)
        else:
            message = 'invalid account or your usertype is not selected correctly'
            return render_template('login.html',message = message)
        

@userBP.route('/changepsw',methods=['GET','POST'])
def setPassword():
    if request.method == 'GET':
        if userPublic.username == '' or userPublic.usertype == 'teacher': 
            
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            
            message = ''
            return render_template('changepsw.html',message = message)
    else:
        oldPsw = request.form.get('exampleInputEmail1')
        newPsw1 = request.form.get('exampleInputPassword1')
        newPsw2 = request.form.get('exampleInputPassword2')
        
        
        if oldPsw == newPsw1:
            message = 'you have not changed your password!'
            return render_template('changepsw.html',message = message)
        result = User.query.filter(and_(User.username == userPublic.username,User.psw == oldPsw)).first()
        if result:
            if newPsw1 == newPsw2:
                result.psw = newPsw1
                db.session.commit()
                return redirect('http://127.0.0.1:5000/user/login') 
            else:
                message = 'different new passwords you have entered'
                return render_template('changepsw.html',message = message)
        else:
                message = 'invalid password'
                return render_template('changepsw.html',message = message)


