from flask import Blueprint,render_template, request
from app.models.student import Student
from app.models.course_student import Course_student,currentStudent
from app.models.member import Member,currentMember
from app.models.leader import Leader
from app.models.subItem import SubItem,currentSub
from app.models.user import User,userPublic
from flask import redirect
from app.models.course import Course
import psutil
import datetime
import urllib
import json
import random
from sqlalchemy.sql import text
from app.models.base import db
import pymysql
from wtforms.fields import simple
from sqlalchemy import or_,and_,all_,any_
from flask import Blueprint,render_template, request, send_from_directory,Flask,redirect,url_for
from app.models.CourseTeamStudent import CourseTeamStudent
from wtforms import Form, StringField, PasswordField, DateField, validators
import os 


leaderBP = Blueprint('leader',__name__)

@leaderBP.route('/selectcourse', methods=['GET','POST'])
def selectcourse():
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'teacher':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            result = Student.query.filter(Student.Email == userPublic.username).first()
            
            result = result.StudentID#studentid
            currentStudent.studentID = result
            
            courseid = Course_student.query.filter(Course_student.studentID == result).all()
            
            result = []
            for i in courseid:
                coursename = Course.query.filter(Course.CourseId == i.CourseId).all()
                for j in coursename:
                    
                    result.append(j.CourseName)
            if result is None or len(result) is 0:
                result=['undecided']      
            else:
                pass
            return render_template('stuselectcourse.html', result = result,message = message)
    else:
        namecourse = request.form.get('option')
        result = Course.query.filter(Course.CourseName==namecourse).first()
        idcourse = result.CourseId
        currentStudent.CourseId = idcourse
        #查个section找老师
        result = Course_student.query.filter(and_(Course_student.studentID==currentStudent.studentID,Course_student.CourseId==currentStudent.CourseId)).first()
        currentStudent.sectionNo = result.sectionNo
        check = Leader.query.filter(and_(Leader.CourseId == currentStudent.CourseId,Leader.StudentID==currentStudent.studentID)).first()
        if check:
            return redirect('./selectSub')
        else:
            message='You are a member. This path is inavailable for you. Please use evaluate leader button!'
            return render_template('stuprompt.html',message = message)
        

@leaderBP.route('/selectSub', methods=['GET','POST'])
def selectSub():
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'teacher':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            result = Student.query.filter(Student.Email == userPublic.username).first()
            result = result.StudentID#studentid
            currentStudent.studentID = result
            subresult = SubItem.query.filter(and_(SubItem.CourseId==currentStudent.CourseId,SubItem.sectionNo==currentStudent.sectionNo)).all()
            result = []
            for i in subresult:
                result.append(i.sTitle)
            if result is None or len(result) is 0:
                result=['undecided']      
            else:
                pass
            return render_template('submissionlist.html',result = result,message = message)
    else:
        sub = request.form.get('option')
        currentSub.sTitle=sub
        check = SubItem.query.filter(and_(SubItem.CourseId==currentStudent.CourseId,SubItem.sectionNo==currentStudent.sectionNo,SubItem.sTitle==currentSub.sTitle)).first()
        currentSub.percentage = check.percentage
        return redirect('./selectmem')

@leaderBP.route('/selectmem', methods=['GET','POST'])
def selectmem():
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'teacher':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            result = Member.query.filter(and_(Member.CourseId==currentStudent.CourseId,Member.StudentID==currentStudent.studentID)).first()
            tid = result.tid
            result1 = Member.query.filter(and_(Member.CourseId==currentStudent.CourseId,Member.sectionNo==currentStudent.sectionNo,Member.tid == tid)).all()
            feed = []
            for i in result1:
                
                feed.append(i.StudentID)
            return render_template('selectmem.html',message = message,result = feed)
    else:
        currentMember.StudentID=request.form.get('option')
        return redirect('./setContribution')
    
                

@leaderBP.route('/setContribution', methods=['GET','POST'])
def setContribution():
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'teacher':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else: 
            return render_template('setcontribution.html',message = message)
    else:
        points = request.form['evaluate']
        point = 0
        if points=='1':
            point = 1
        elif points=='0.67':
            point=0.67
        elif points=='0.33':
            point=0.33
        elif points=='0':
            point=0
        result = Member.query.filter(and_(Member.StudentID==currentMember.StudentID,Member.CourseId==currentStudent.CourseId)).first()
        already = result.default
        if already == 0:
            result.contribution = result.contribution+point*currentSub.percentage*0.01
            db.session.commit()
        else:
            result.contribution = point*currentSub.percentage*0.01
            result.default = 0
            db.session.commit()
        message = 'You have evaluated %s!'%(currentMember.StudentID)
        return render_template('setcontribution.html',message = message)

