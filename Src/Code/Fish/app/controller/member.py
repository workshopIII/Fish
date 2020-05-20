from flask import Blueprint,render_template, request
from app.models.student import Student
from app.models.course_student import Course_student,currentStudent
from app.models.member import Member
from app.models.leader import Leader
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

memberBP = Blueprint('member',__name__)

@memberBP.route('/voteselectCourse', methods=['GET','POST'])
def voteselectCourse():
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'teacher':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
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
        return redirect('./voteleader')

@memberBP.route('/voteleader', methods=['GET','POST'])
def voteleader():
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'teacher':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            #把组员找出来
            result = Member.query.filter(and_(Member.CourseId==currentStudent.CourseId,Member.StudentID==currentStudent.studentID)).first()
            feed = []
            if result:
                tid = result.tid
                result1 = Member.query.filter(and_(Member.CourseId==currentStudent.CourseId,Member.sectionNo==currentStudent.sectionNo,Member.tid == tid)).all()
                for i in result1:
                    feed.append(i.StudentID)
            else:
                pass
            return render_template('voteleader.html',message = message,result = feed)
    else:
        leader =  request.form.get('option')#get的学号
        check = Member.query.filter(and_(Member.CourseId==currentStudent.CourseId,Member.StudentID==currentStudent.studentID)).first()
        check.vote = leader
        db.session.commit()
        result = Member.query.filter(and_(Member.CourseId==currentStudent.CourseId,Member.StudentID==currentStudent.studentID)).first()
        tid = result.tid
        result1 = Member.query.filter(and_(Member.CourseId==currentStudent.CourseId,Member.sectionNo==currentStudent.sectionNo,Member.tid == tid)).all()
        feed = []
        for i in result1:
            feed.append(i.StudentID)
        message = 'You have submitted your selection!'
        return render_template('voteleader.html',message = message,result = feed)

@memberBP.route('/redovote', methods=['GET','POST'])
def redovote():
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'teacher':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            result = Member.query.filter(and_(Member.CourseId==currentStudent.CourseId,Member.StudentID==currentStudent.studentID)).first()
            result.vote = ''
            db.session.commit()
            result = Member.query.filter(and_(Member.CourseId==currentStudent.CourseId,Member.StudentID==currentStudent.studentID)).first()
            tid = result.tid
            result1 = Member.query.filter(and_(Member.CourseId==currentStudent.CourseId,Member.sectionNo==currentStudent.sectionNo,Member.tid == tid)).all()
            feed = []
            for i in result1:
                feed.append(i.StudentID)
            
            return redirect('./voteleader')
    else:
        pass

@memberBP.route('/viewresult', methods=['GET','POST'])
def viewresult():
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
            maxone = 0
            maxstu =''
            for i in result1:
                count = Member.query.filter(and_(Member.CourseId==currentStudent.CourseId,Member.sectionNo==currentStudent.sectionNo,Member.tid == tid,Member.vote==i.StudentID)).count()
                if maxone<count:
                    maxone = count
                    maxstu = i.StudentID
            result =  Member.query.filter(and_(Member.CourseId==currentStudent.CourseId,Member.StudentID==maxstu)).first()
            tid = result.tid
            count = Leader.query.order_by(-Leader.lid).first()
            if count:
                lid = count.lid+1
            else:
                lid = 1
            result = Leader.query.filter(and_(Leader.CourseId==currentStudent.CourseId,Leader.sectionNo == currentStudent.sectionNo, Leader.Tid==tid)).first()
            if result:
                result.StudentID=maxstu
                db.session.commit()
            else:
                addition = Leader(lid,maxstu,currentStudent.CourseId,currentStudent.sectionNo,tid,0.0,0.0,1)
                db.session.add(addition)
                db.session.commit()
            message = 'The leader in group %d in course %s is %s'%(tid,currentStudent.CourseId,maxstu)
            return render_template('voteresult.html',message = message)
    else:
        pass

@memberBP.route('/eselectcourse', methods=['GET','POST'])
def eselectcourse():
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'teacher':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
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
            message='You are a leader. This path is inavailable for you. Please use evaluate member button!'
            return render_template('stuprompt.html',message = message)
        else:
            return redirect('./eleader')

@memberBP.route('/eleader', methods=['GET','POST'])
def eleader():
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'teacher':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            check = Leader.query.filter(and_(Leader.CourseId == currentStudent.CourseId,Leader.StudentID==currentStudent.studentID)).first()
            if check:
                message='You are a leader. This path is inavailable for you. Please use evaluate member button!'
                return render_template('stuprompt.html',message = message)
            else:
                return render_template('evaluateleader.html',message = message)
    else:
        points = request.form['evaluate']
        point = 0
        if points=='2':
            point = 2
        elif points=='1':
            point=1
        elif points=='0':
            point=0
        elif points=='-1':
            point=-1
        elif points=='-2':
            point = -2
        checkteam = Member.query.filter(and_(Member.CourseId==currentStudent.CourseId,Member.StudentID==currentStudent.studentID)).first()
        tid = checkteam.tid
        
        checkleader = Leader.query.filter(and_(Leader.CourseId==currentStudent.CourseId, Leader.sectionNo == currentStudent.sectionNo,Leader.Tid==tid)).first()
        already = checkleader.default
        if already==0:
            checkleader.bonus = (checkleader.bonus+point)/2
            db.session.commit()
        else:
            checkleader.bonus = point
            checkleader.default=0
            db.session.commit()
        message = 'You have evaluated your leader!'
        return render_template('evaluateleader.html',message = message)

