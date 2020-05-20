from flask import Blueprint,render_template, request
from app.models.base import db
from app.models.course import Course
from app.models.teacher import Teacher
from app.models.user import User,userPublic
from app.models.course_teacher import Course_teacher,currentCourse
from flask import Flask,render_template,request,redirect,url_for
from sqlalchemy import or_,and_,all_,any_


courseBP = Blueprint('course',__name__)

@courseBP.route('/changecoursename', methods=['GET','POST'])
def changecoursename():
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            result = Teacher.query.filter(Teacher.email == userPublic.username).first()
            
            result = result.staffid#90641857
            courseid = Course_teacher.query.filter(Course_teacher.staffID == result).all()
            
            result = []
            for i in courseid:
                coursename = Course.query.filter(Course.CourseId == i.CourseId).all()
                for j in coursename:
                    
                    result.append(j.CourseName)
            if result is None or len(result) is 0:
                result=['undecided']      
            else:
                pass
            return render_template('changeCourseName.html',result = result, message = message)
    else:
        namecourse = request.form.get('option')
        newcoursename = request.form.get('coursename')
        if namecourse == newcoursename:
            message='you enter the same course name as the old one!'
            result = Teacher.query.filter(Teacher.email == userPublic.username).first()
            
            result = result.staffid#90641857
            courseid = Course_teacher.query.filter(Course_teacher.staffID == result).all()
                
            result = []
            for i in courseid:
                coursename = Course.query.filter(Course.CourseId == i.CourseId).all()
                for j in coursename:
                        
                    result.append(j.CourseName)
            if result is None or len(result) is 0:
                    result=['undecided']      
            else:
                pass
            return render_template('changeCourseName.html',result = result, message = message)
        else:
            result = Course.query.filter(Course.CourseName==namecourse).first()
            result.CourseName = newcoursename
            db.session.commit()
            message = 'Course name changed!'
            result = Teacher.query.filter(Teacher.email == userPublic.username).first()
            
            result = result.staffid#90641857
            courseid = Course_teacher.query.filter(Course_teacher.staffID == result).all()
                
            result = []
            for i in courseid:
                coursename = Course.query.filter(Course.CourseId == i.CourseId).all()
                for j in coursename:
                        
                    result.append(j.CourseName)
            if result is None or len(result) is 0:
                result=['undecided']      
            else:
                pass
            return render_template('changeCourseName.html',result = result, message = message)
