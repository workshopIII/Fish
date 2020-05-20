import psutil
import xlwt
import datetime
import urllib
import json
import pymysql
from wtforms.fields import simple
from sqlalchemy import or_,and_,all_,any_
from flask import Blueprint,render_template, request, send_from_directory
from app.models.base import db
from werkzeug.utils import secure_filename
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.user import User,userPublic
from app.models.course_teacher import Course_teacher,currentCourse
from app.models.course_student import Course_student
from app.models.invitation import Invitation
from app.models.member import Member
from app.models.leader import Leader
from app.models.course import Course
from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
from wtforms import Form, StringField, PasswordField, DateField, validators
import os 
import pymysql
import xlrd


filesBP = Blueprint('files',__name__)

@filesBP.route('/importf', methods=['GET','POST'])
def import_f():
    if request.method == 'GET' :
        result = ''
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
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
            return render_template('importclassinfo.html', result = result,message = message)        
    else:
        namecourse = request.form.get('option')
        print('see what is the namecourse')
        print(namecourse)
        result = Course.query.filter(Course.CourseName==namecourse).first()
        print('see what is in the courseid')
        print(result)
        idcourse = result.CourseId
        result = Teacher.query.filter(Teacher.email==userPublic.username).first()
        idstaff = result.staffid
        result = Course_teacher.query.filter(and_(Course_teacher.staffID==idstaff,Course_teacher.CourseId==idcourse)).first()
        section = result.sectionNo
        f = request.files['file']
        #basepath = sys.path[0]
        #upload_path = os.path.join(basepath,'files',secure_filename(f.filename)) 
        #filename = f.filename
        f.save(secure_filename(f.filename))
        fname=f.filename.split('.')[0]
        book = xlrd.open_workbook(f.filename)
        sheet = book.sheet_by_name(fname)
        for r in range(0, sheet.nrows):
            email = sheet.cell(r,0).value
            studentid = sheet.cell(r,1).value
            studentname = sheet.cell(r,2).value
            stugpa = sheet.cell(r,3).value
            check = Student.query.filter(Student.StudentID==studentid).first()
            #Student table primary key check unique
            print(check)
            if check:

                message = 'already have the data in Student table'
            else:
                result = Student(studentid,studentname,email,stugpa)
                db.session.add(result)
                db.session.commit()
            
            check1 = User.query.filter(User.username==email).first()
            print(check1)
            if check1:
                message = 'already have the data in User table'
            else:
                result1 = User(email,'123456','student')
                db.session.add(result1)
                db.session.commit()
            check2 = Course_student.query.filter(and_(Course_student.studentID==studentid,Course_student.CourseId==idcourse)).first()
            print(check2)
            if check2:
                message = 'already have the data in Course_student table'
            else:
                rid = Course_student.query.order_by(-Course_student.rrrid).first()
                if rid:
                    rid=rid.rrrid+1
                else:
                    rid=1
                result2 = Course_student(rid,studentid,idcourse,section)
                db.session.add(result2)
                db.session.commit()   
                message = 'import '+f.filename+' into database!'
            #把这个班的学生名单先加入invitation的studentID里面
            
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
        check4 = Invitation.query.filter(and_(Invitation.studentID==studentid,Invitation.CourseId==idcourse)).first()
        if check4:
            pass
        else:
            listresult= Course_student.query.filter(and_(Course_student.CourseId==idcourse,Course_student.sectionNo==section)).all()
            for i in listresult:
                count = Invitation.query.count()
                addition = Invitation(count+1,idcourse,section,i.studentID,'',0)
                db.session.add(addition)
                db.session.commit()
        return render_template('importclassinfo.html', message = message,result = result)

@filesBP.route('/exportf', methods=['GET','POST'])
def exportf():
    if request.method == 'GET' :
        result = ''
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
            return render_template('export.html', result = result,message = message) 
    else:
        namecourse = request.form.get('option')
        result = Course.query.filter(Course.CourseName==namecourse).first()
        print('see what is in the courseid')
        print(result)
        currentCourse.CourseId = result.CourseId
        result = Teacher.query.filter(Teacher.email==userPublic.username).first()
        currentCourse.staffID = result.staffid
        result = Course_teacher.query.filter(and_(Course_teacher.staffID==currentCourse.staffID,Course_teacher.CourseId==currentCourse.CourseId)).first()
        currentCourse.sectionNo = result.sectionNo
        row1result = Member.query.filter(and_(Member.CourseId==currentCourse.CourseId,Member.sectionNo==currentCourse.sectionNo)).all()
        row2 = []
        row1 = []
        row3 = []
        row4 = []
        for i in row1result:
            nameresult = Student.query.filter(Student.StudentID==i.StudentID).first()
            row1.append(nameresult.StuName)
            row2.append(i.StudentID)
            row3.append(i.contribution)
            result = Leader.query.filter(and_(Leader.CourseId==currentCourse.CourseId,Leader.StudentID==i.StudentID)).first()
            if result:
                row4.append(result.bonus)
            else:
                row4.append(0)
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet1 = workbook.add_sheet("exportfile")
        sheet1.write(0,0,"studentName")
        sheet1.write(0,1,"studentID")
        sheet1.write(0,2,"contribution")
        sheet1.write(0,3,"bonus")
        num=1
        for i in row1:
            sheet1.write(num,0,i)
            num = num+1
        num = 1
        for i in row2:
            sheet1.write(num,1,i)
            num = num+1
        num=1
        for i in row3:
            sheet1.write(num,2,i)
            num=num+1
        num=1
        for i in row4:
            sheet1.write(num,3,i)
            num = num+1
        workbook.save(r'C:\Users\hp\Desktop\workshop\controller\files\export.xls')
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
        message = 'file exported!'
        return render_template('export.html', result = result,message = message)

       

