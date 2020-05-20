from app.models.divideIn import DivideIn,division
from app.models.user import userPublic
from app.models.course_teacher import Course_teacher,currentCourse
from app.models.course_student import Course_student,currentStudent
from app.models.teacher import Teacher,teacherPublic
from app.models.student import Student
from app.models.member import Member
import psutil
import datetime
import urllib
import json
import random
from sqlalchemy.sql import text
import pymysql
from wtforms.fields import simple
from sqlalchemy import or_,and_,all_,any_
from flask import Blueprint,render_template, request, send_from_directory,Flask,redirect,url_for
from app.models.base import db
from app.models.user import User,userPublic
from app.models.course_teacher import Course_teacher
from app.models.randNumber import RandNumber
from app.models.course_student import Course_student
from app.models.invitation import Invitation
from app.models.CourseTeamStudent import CourseTeamStudent
from app.models.course import Course
from wtforms import Form, StringField, PasswordField, DateField, validators
import os 

divideInBP = Blueprint('divideIn',__name__)

full = []
special1 = 0
@divideInBP.route('/selectCourse', methods=['GET','POST'])
def selectCourse():
    if request.method == 'GET':
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
            division.staffID = result
            currentCourse.staffID = result
            print("here I want to check the reult of division.staffID")
            print(type(division.staffID))
            print(division.staffID)
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
            return render_template('selectCourse.html', result = result,message = message)
    else:
        namecourse = request.form.get('option')
        result = Course.query.filter(Course.CourseName==namecourse).first()
        currentCourse.CourseId = result.CourseId
        result1 = Course_teacher.query.filter(Course_teacher.CourseId==result.CourseId).first()
        currentCourse.sectionNo = result1.sectionNo
        division.CourseId = result.CourseId
        print('here I first check the result of the division.CourseId')
        print(type(division.CourseId))
        print(division.CourseId)
        check = DivideIn.query.filter(and_(DivideIn.CourseId==currentCourse.CourseId,DivideIn.staffID==currentCourse.staffID)).first()
        if check:
            if check.methodNo==3:
                return redirect('./formGroup')
            elif check.methodNo==1 or check.methodNo==2:
                
                
                return redirect('./showresult')
        else:
            return redirect('./enterDnumber')

@divideInBP.route('/enterDnumber', methods=['GET','POST'])
def enterDnumber():
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
        return render_template('enternumofgroup.html',message = message)
    else:
        keyNumber=request.form.get('total')
        if keyNumber == 0:
            message='the number cannot be zero, please enter again!'
            return render_template('enternumofgroup.html', message = message)
        else:
            division.numberPergroup = keyNumber
            division.totalStu = Course_student.query.filter(Course_student.CourseId==currentCourse.CourseId).count()
            division.rest = int(division.totalStu)%int(division.numberPergroup) 
            
            print("I want to see the result of division.rest")
            print(type(division.rest))
            print(division.rest)
            if division.rest == 0:
                division.totalGroup = int(division.totalStu)//int(division.numberPergroup)
                division.groupNNormal= 0
                division.rest = 0
                check = DivideIn.query.filter(and_(DivideIn.CourseId ==division.CourseId,DivideIn.staffID == division.staffID)).first()
                if check:
                    didresult = DivideIn.query.order_by(-DivideIn.did).first()
                    did = didresult.did+1
                    check.did=did
                    check.methodNo = 0
                    check.numberPergroup = int(division.numberPergroup)
                    check.totalStu = int(division.totalStu)
                    check.rest =int(division.rest)
                    check.groupNNormal = int(division.groupNNormal)
                    check.totalGroup = int(division.totalGroup)
                    db.session.commit()
                else:
                    didresult = DivideIn.query.order_by(-DivideIn.did).first()
                    if didresult:
                        did = didresult.did+1
                    else:
                        did = 1
                    result = DivideIn(did,division.CourseId,division.staffID,0,int(division.numberPergroup),int(division.totalStu),int(division.rest),int(division.groupNNormal),int(division.totalGroup))
                    db.session.add(result)
                    db.session.commit()
                return redirect('./selectMethod')
            else:
                return redirect('./suggestion')


@divideInBP.route('/suggestion', methods=['GET','POST'])
def suggestion():
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            division.totalGroup = int(division.totalStu)//int(division.numberPergroup) + 1
            message1 = 'System would divide your class into %d groups, including %d groups with %d members per group and one group with %d members'%(int(division.totalGroup),int(division.totalStu)//int(division.numberPergroup),int(division.numberPergroup),int(division.rest))
            division.totalGroup = int(division.totalStu)//int(division.numberPergroup)
            message2 = 'System would divide your class into %d groups, including %d groups with %d members per group and %d groups with %d members'%(int(division.totalGroup),int(division.totalStu)//int(division.numberPergroup)-int(division.rest),int(division.numberPergroup),int(division.rest),int(division.numberPergroup)+1)
            return render_template('suggestion.html',message1 = message1, message2 = message2)
    else:
        choice = request.form['role']
        if choice == '1':
            division.totalGroup = int(division.totalStu)//int(division.numberPergroup) + 1
            division.groupNNormal = int(division.rest)
        if choice =='2':
            division.totalGroup = int(division.totalStu)//int(division.numberPergroup)
            division.groupNNormal= int(division.numberPergroup)+1
        check = DivideIn.query.filter(and_(DivideIn.CourseId ==division.CourseId,DivideIn.staffID == division.staffID)).first()
        if check:
            check.methodNo = 0
            check.numberPergroup = int(division.numberPergroup)
            check.totalStu = int(division.totalStu)
            check.rest =int(division.rest)
            check.groupNNormal = int(division.groupNNormal)
            check.totalGroup = int(division.totalGroup)
            db.session.commit()
        else:
            didresult = DivideIn.query.order_by(-DivideIn.did).first()
            if didresult:
                did = didresult.did+1
            else:
                did = 1
            result = DivideIn(did,division.CourseId,division.staffID,0,int(division.numberPergroup),int(division.totalStu),int(division.rest),int(division.groupNNormal),int(division.totalGroup))
            print('suggestion')
            print('division.CourseId')
            print(division.CourseId)
            print('division.staffID')
            print(division.staffID)
            db.session.add(result)
            db.session.commit()
        return redirect('./selectMethod')

@divideInBP.route('/selectMethod', methods=['GET','POST'])
def selectMethod():
    if request.method == 'GET':
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
        return render_template('choosemethod.html')
    else:
        pass

@divideInBP.route('/method1', methods=['GET'])#devide by system
def method1():
    if request.method == 'GET':
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            result = DivideIn.query.filter(and_(DivideIn.CourseId == currentCourse.CourseId,DivideIn.staffID==currentCourse.staffID)).first()
            result.methodNo = 1
            db.session.commit()
            count= RandNumber.query.count()
            if count!=0:   
                print(type(count))
                print(count)
                for i in range(0,count):
                    obj = RandNumber.query.filter(RandNumber.listid==i+1).first()
                    db.session.delete(obj)
                    db.session.commit()
            if int(division.rest)==0:
                
                #每个数字随机生成numberPergroup个
                while(RandNumber.query.count()<division.totalStu):
                    
                    num = random.randint(1,division.totalGroup)
                    result = RandNumber.query.filter(RandNumber.num==num).count()
                    if result < int(division.numberPergroup):
                        writein = RandNumber(RandNumber.query.count()+1,num)
                        db.session.add(writein)
                        db.session.commit()
                    else:
                        continue
            else:
                if int(division.totalStu)//int(division.numberPergroup) < int(division.totalGroup):
                    #一个组的人数不同于其他组
                    full = []
                    while(RandNumber.query.count()<division.totalStu):
                        
                        num = random.randint(1,division.totalGroup)#生成随机数
                        result = RandNumber.query.filter(RandNumber.num==num).count()#数现在跟这个随机数相等的有几个
                        if  len(full)<1:
                            if result < int(division.groupNNormal): 
                                writein = RandNumber(RandNumber.query.count()+1,num)
                                db.session.add(writein)
                                db.session.commit()
                                result = RandNumber.query.filter(RandNumber.num==num).count()
                                if result == int(division.groupNNormal):
                                    full.append(num)
                                else:
                                    continue
                            else:
                                continue
                        else:
                            if result < int(division.numberPergroup):
                                writein = RandNumber(RandNumber.query.count()+1,num)
                                db.session.add(writein)
                                db.session.commit()
                            else:
                                continue
                            
                            
                elif int(division.totalStu)//int(division.numberPergroup) == int(division.totalGroup):
                    full = []
                    while(RandNumber.query.count()<division.totalStu):
                        num = random.randint(1,division.totalGroup)#随机组数
                        result = RandNumber.query.filter(RandNumber.num==num).count()#这个组数的数量
                        #组数等于groupNNormal而且等于groupNNormal的组的数量不到rest个
                        if len(full)<int(division.rest):
                            if result < int(division.groupNNormal):
                                writein = RandNumber(RandNumber.query.count()+1,num)
                                db.session.add(writein)
                                db.session.commit()
                                result = RandNumber.query.filter(RandNumber.num==num).count()
                                if result == int(division.groupNNormal):
                                    full.append(num)
                                else:
                                    continue
                            else:
                                continue
                        else:
                            if result<int(division.numberPergroup):
                                writein = RandNumber(RandNumber.query.count()+1,num)
                                db.session.add(writein)
                                db.session.commit()
                            else:
                                continue
                        
            
            result = RandNumber.query.first()
            listid = result.listid
            
            sectionresult = Course_teacher.query.filter(and_(Course_teacher.staffID == division.staffID,Course_teacher.CourseId == division.CourseId)).first()
            section = sectionresult.sectionNo
            #整个班的学生
            allresult = Course_student.query.filter(and_(Course_student.CourseId == division.CourseId,Course_student.sectionNo==section)).all()
            #确定rid
            rid = 0
            for i in allresult:
                count = CourseTeamStudent.query.filter(and_(Course_student.CourseId == division.CourseId,Course_student.sectionNo==section)).order_by(-CourseTeamStudent.rid).first()
                if count:
                    rid = count.rid+1
                else:
                    count = CourseTeamStudent.query.order_by(-CourseTeamStudent.rid).first()
                    if count:
                        rid = count.rid+1
                    else:
                        rid = 1
                num = RandNumber.query.filter(RandNumber.listid == listid).first()
                tid = num.num
                stu = i.studentID
                listid=listid+1
                result = CourseTeamStudent(rid=rid,CourseId = division.CourseId,Tid = tid, StudentID =stu, sectionNo=currentCourse.sectionNo)
                db.session.add(result)
                db.session.commit()
            
            #把CourseTeamStudent里面的数据放进member里面
            
            select = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==currentCourse.CourseId,CourseTeamStudent.sectionNo==currentCourse.sectionNo)).all()
            for i in select:
                number = Member.query.count()
                result = Member(number+1,i.StudentID,i.CourseId,i.sectionNo,1.0,i.Tid,'',1)
                db.session.add(result)
                db.session.commit()
            
            #删除随机数的数据库
            num = RandNumber.query.count()
            print(type(num))
            print(num)
            for i in range(0,num):
                obj = RandNumber.query.filter(RandNumber.listid==i+1).first()
                db.session.delete(obj)
                db.session.commit()
        return redirect('./showresult')

@divideInBP.route('/showresult', methods=['GET'])
def showresult():
    if request.method == 'GET':
        if userPublic.username == '':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            result1 = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId == division.CourseId,CourseTeamStudent.sectionNo==currentCourse.sectionNo)).order_by(CourseTeamStudent.Tid).all()
            feed = []
            for i in result1:
                msg = []
                msg.append(i.CourseId)
                msg.append(i.Tid)
                msg.append(i.StudentID)
                feed.append(msg)
        return render_template('displaygroup.html',result = feed)
    else:
        pass
            
@divideInBP.route('/warning', methods=['GET','POST'])
def warning():
    if request.method == 'GET':
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            message = 'If redo the process, your current form group result would be deleted. Are you sure to redo?'
        return render_template('warning.html',message = message)
    else:
        pass  

@divideInBP.route('/redo', methods=['GET','POST'])
def redo():
    if request.method == 'GET':
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            deresult = DivideIn.query.filter(and_(DivideIn.CourseId==currentCourse.CourseId,DivideIn.staffID==division.staffID)).first()
            print('redo')
            print(deresult)
            if deresult:
                db.session.delete(deresult)
                db.session.commit()
            else:
                pass
            opresult = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==division.CourseId,CourseTeamStudent.sectionNo==currentCourse.sectionNo)).first()
            if opresult:
                op = opresult.rid
                num = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==division.CourseId,CourseTeamStudent.sectionNo==currentCourse.sectionNo)).count()
                for i in range(0,num):
                    obj = CourseTeamStudent.query.filter(CourseTeamStudent.rid==op).first()
                    db.session.delete(obj)
                    db.session.commit()
                    op=op+1
            else:
                pass
            opresult = Invitation.query.filter(and_(Invitation.CourseId==currentCourse.CourseId,Invitation.sectionNo==currentCourse.sectionNo)).first()
            if opresult:
                op = opresult.iid
                num = Invitation.query.filter(and_(Invitation.CourseId==currentCourse.CourseId,Invitation.sectionNo==currentCourse.sectionNo)).count()
                for i in range(num):
                    obj = Invitation.query.filter(Invitation.iid==op).first()
                    obj.studentID = ''
                    obj.confirm = 0
                    db.session.commit()
            else:
                pass
            #member 相关数据清空
            check = Member.query.filter(and_(Member.CourseId==currentCourse.CourseId,Member.sectionNo==currentCourse.sectionNo)).all()
            if check:
                for i in check:
                    db.session.delete(i)
                    db.session.commit()

        return redirect('./selectCourse')
    else:
        pass  

@divideInBP.route('/checkresult', methods=['GET','POST'])
def checkresult():
    if request.method == 'GET':
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            result = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId == currentCourse.CourseId,CourseTeamStudent.sectionNo == currentCourse.sectionNo)).first()
            if result:
                return redirect('./showresult')
            else:
                return redirect('./selectCourse')
    else:
        pass 

@divideInBP.route('/studentGroup', methods=['GET','POST'])
def studentGroup():
    if request.method == 'GET':
        if userPublic.username == '' or userPublic.usertype == 'teacher':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            result1 = Course_teacher.query.filter(and_(Course_teacher.CourseId==currentStudent.CourseId,Course_teacher.sectionNo==currentStudent.sectionNo)).first()
            currentCourse.staffID = result1.staffID
            result = DivideIn.query.filter(and_(DivideIn.CourseId == currentStudent.CourseId,DivideIn.staffID==currentCourse.staffID)).first()
            if result:
                if result.methodNo == 1:
                    result1 = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId == currentStudent.CourseId,CourseTeamStudent.sectionNo==currentStudent.sectionNo)).order_by(CourseTeamStudent.Tid).all()
                    feed = []
                    print('studentGroup')
                    print(division.CourseId)
                    print(currentStudent.sectionNo)
                    print(result1)
                    for i in result1:
                        msg = []
                        msg.append(i.CourseId)
                        msg.append(i.Tid)
                        msg.append(i.StudentID)
                        feed.append(msg)
                    return render_template('studisplaygroup.html',result = feed)
                elif result.methodNo == 2:
                    return render_template('studentGroup.html')
                elif result.methodNo == 3:
                    return render_template('friendSystem.html')
            else:
                message = 'There is no form group dicision in this course'
                return render_template('stuprompt.html',message=message)

    else:
        pass 

@divideInBP.route('/stuSelectCourse', methods=['GET','POST'])
def stuSelectCourse():
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
        #先查form group method有没有定，选1的话直接跳到display，选2是下面这个return，0的话直接prompt说还没有进行决定
        
        return redirect('./studentGroup')


@divideInBP.route('/method2', methods=['GET','POST'])
def method2():
    if request.method == 'GET':
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            result = DivideIn.query.filter(and_(DivideIn.CourseId == currentCourse.CourseId,DivideIn.staffID==currentCourse.staffID)).first()
            result.methodNo = 2
            db.session.commit()
            result = Course_teacher.query.filter(and_(Course_teacher.CourseId == currentCourse.CourseId,Course_teacher.sectionNo==currentCourse.sectionNo)).first()
            idstaff = result.staffID
            result1 = DivideIn.query.filter(and_(DivideIn.CourseId==currentCourse.CourseId,DivideIn.staffID==idstaff)).first()
            division.totalGroup = result1.totalGroup
            division.rest = result1.rest
            division.numberPergroup = result1.numberPergroup
            division.totalStu = result1.totalStu
            division.groupNNormal = result1.groupNNormal
            #在使用RandNumber之前先清空
            count= RandNumber.query.count()
            if count!=0:   
                print(type(count))
                print(count)
                for i in range(0,count):
                    obj = RandNumber.query.filter(RandNumber.listid==i+1).first()
                    db.session.delete(obj)
                    db.session.commit()
            #使用RandNumber表格
            if int(division.rest)==0:
                
                #每个数字随机生成numberPergroup个
                while(RandNumber.query.count()<division.totalStu):
                    
                    num = random.randint(1,division.totalGroup)
                    result = RandNumber.query.filter(RandNumber.num==num).count()
                    if result < int(division.numberPergroup):
                        writein = RandNumber(RandNumber.query.count()+1,num)
                        db.session.add(writein)
                        db.session.commit()
                    else:
                        continue

            else:
                if int(division.totalStu)//int(division.numberPergroup) < int(division.totalGroup):
                    #一个组的人数不同于其他组
                    full = []
                    while(RandNumber.query.count()<division.totalStu):
                        
                        num = random.randint(1,division.totalGroup)#生成随机数
                        result = RandNumber.query.filter(RandNumber.num==num).count()#数现在跟这个随机数相等的有几个
                        if  len(full)<1:
                            if result < int(division.groupNNormal): 
                                writein = RandNumber(RandNumber.query.count()+1,num)
                                db.session.add(writein)
                                db.session.commit()
                                result = RandNumber.query.filter(RandNumber.num==num).count()
                                if result == int(division.groupNNormal):
                                    full.append(num)
                                else:
                                    continue
                            else:
                                continue
                        else:
                            if result < int(division.numberPergroup):
                                writein = RandNumber(RandNumber.query.count()+1,num)
                                db.session.add(writein)
                                db.session.commit()
                            else:
                                continue
                            
                            
                elif int(division.totalStu)//int(division.numberPergroup) == int(division.totalGroup):
                    full = []
                    while(RandNumber.query.count()<division.totalStu):
                        num = random.randint(1,division.totalGroup)#随机组数
                        result = RandNumber.query.filter(RandNumber.num==num).count()#这个组数的数量
                        #组数等于groupNNormal而且等于groupNNormal的组的数量不到rest个
                        if len(full)<int(division.rest):
                            if result < int(division.groupNNormal):
                                writein = RandNumber(RandNumber.query.count()+1,num)
                                db.session.add(writein)
                                db.session.commit()
                                result = RandNumber.query.filter(RandNumber.num==num).count()
                                if result == int(division.groupNNormal):
                                    full.append(num)
                                else:
                                    continue
                            else:
                                continue
                        else:
                            if result<int(division.numberPergroup):
                                writein = RandNumber(RandNumber.query.count()+1,num)
                                db.session.add(writein)
                                db.session.commit()
                            else:
                                continue
            
            message = 'Waiting for students to choose their groups. '
            return render_template('warning.html',message = message)
    else:
        pass

@divideInBP.route('/chooseGroup', methods=['GET','POST'])
def chooseGroup():
    
    #full里面的数字的组别的人数是numberPerGroup+1 
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'teacher':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            full = []
            result = Course_teacher.query.filter(and_(Course_teacher.CourseId == currentStudent.CourseId,Course_teacher.sectionNo==currentStudent.sectionNo)).first()
            idstaff = result.staffID
            result1 = DivideIn.query.filter(and_(DivideIn.CourseId==currentStudent.CourseId,DivideIn.staffID==idstaff)).first()
            division.totalGroup = result1.totalGroup
            division.rest = result1.rest
            division.numberPergroup = result1.numberPergroup
            division.totalStu = result1.totalStu
            division.groupNNormal = result1.groupNNormal
            print('division.totalGroup')
            print(division.totalGroup)
            print(type(division.totalGroup))
            
            for i in range(division.totalGroup):
                count = RandNumber.query.filter(RandNumber.num==i+1).count()
                
                if int(division.totalStu)//int(division.numberPergroup) < int(division.totalGroup):
                    if count==division.rest:
                        special1=i+1#groupNNormal
                elif int(division.totalStu)//int(division.numberPergroup) == int(division.totalGroup):
                    if count==division.groupNNormal:
                        full.append(i+1)#groupNNormal组
            print('full')
            print(full)
            result = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==currentStudent.CourseId,CourseTeamStudent.StudentID==currentStudent.studentID)).first()
            if result:
                return redirect('./viewresult')
                        
            else:
                choice = []
                for i in range(0,int(division.totalGroup)):
                    choice.append(i+1)
                if int(division.rest)==0:
                    message = ''
                elif int(division.totalStu)//int(division.numberPergroup) < int(division.totalGroup):
                    message = 'group %d could only has %d members and other groups have %d members per group'%(special1,int(division.rest),int(division.numberPergroup))
                elif int(division.totalStu)//int(division.numberPergroup) == int(division.totalGroup):
                    info = ''
                    for i in range(len(full)):
                        print('i')
                        print(i)
                        info = info + '%d '%(full[i])
                    print('info')
                    print(info)
                    message = 'Group ' + info + 'have %d members per group and other groups have %d members per group'%(int(division.groupNNormal),int(division.numberPergroup))
                return render_template('chooseGroup.html',result = choice, message = message)
    else:
        full = []
        for i in range(division.totalGroup):
            count = RandNumber.query.filter(RandNumber.num==i+1).count()
                
            if int(division.totalStu)//int(division.numberPergroup) < int(division.totalGroup):
                if count==division.rest:
                    special1=i+1#groupNNormal
            elif int(division.totalStu)//int(division.numberPergroup) == int(division.totalGroup):
                if count==division.groupNNormal:#groupNNormal组
                    full.append(i+1)
        group = request.form.get('option') 
        choice = []
        for i in range(0,int(division.totalGroup)):
            choice.append(i+1)
        num = CourseTeamStudent.query.filter(and_(CourseTeamStudent.Tid==group,CourseTeamStudent.CourseId == currentStudent.CourseId)).count()
        select = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==currentStudent.CourseId,CourseTeamStudent.sectionNo==currentStudent.sectionNo)).first()
        number = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==currentStudent.CourseId,CourseTeamStudent.sectionNo==currentStudent.sectionNo)).count()
        if select:
            rid = select.rid+number-2
        else:
            check = CourseTeamStudent.query.count()
            rid = check+1
        if int(division.rest)==0:
            if num==int(division.numberPergroup):
                message = 'the group you have chosen is full, please make another choice!'
                return render_template('chooseGroup.html',result = choice, message = message)
            else:
                #rid = num+1
                addition = CourseTeamStudent(rid,currentStudent.CourseId,group,currentStudent.studentID,currentStudent.sectionNo)
                db.session.add(addition)
                db.session.commit()
                number = Member.query.count()
                addition2 = Member(number+1,currentStudent.studentID,currentStudent.CourseId,currentStudent.sectionNo,1.0,group,'',1)
                db.session.add(addition2)
                db.session.commit()
                message = 'You have chosen group %d!'%(int(group))
                return render_template('chooseGroup.html',result = choice, message = message)
        else:
            if int(division.totalStu)//int(division.numberPergroup) < int(division.totalGroup):
                if group==special1 and num==int(division.rest):
                   message = 'the group you have chosen is full, please make another choice!'
                   return render_template('chooseGroup.html',result = choice, message = message)
                elif group!=special1 and num == int(division.numberPergroup):
                   message = 'the group you have chosen is full, please make another choice!'
                   return render_template('chooseGroup.html',result = choice, message = message)
                else:
                    addition = CourseTeamStudent(rid,currentStudent.CourseId,group,currentStudent.studentID,currentStudent.sectionNo)
                    db.session.add(addition)
                    db.session.commit()
                    number = Member.query.count()
                    addition2 = Member(number+1,currentStudent.studentID,currentStudent.CourseId,currentStudent.sectionNo,1.0,group,'',1)
                    db.session.add(addition2)
                    db.session.commit()
                    message = 'You have chosen group %d!'%(int(group))
                    return render_template('chooseGroup.html',result = choice, message = message)
            elif int(division.totalStu)//int(division.numberPergroup) == int(division.totalGroup):
                for i in full:
                    if group==i and num==int(division.groupNNormal):
                        message = 'the group you have chosen is full, please make another choice!'
                        return render_template('chooseGroup.html',result = choice, message = message)
                    elif group==i and num<int(division.groupNNormal):
                        addition = CourseTeamStudent(rid,currentStudent.CourseId,group,currentStudent.studentID,currentStudent.sectionNo)
                        db.session.add(addition)
                        db.session.commit()
                        message = 'You have chosen group %d!'%(int(group))
                        return render_template('chooseGroup.html',result = choice, message = message)
                if num==int(division.numberPergroup):
                    message = 'the group you have chosen is full, please make another choice!'
                    return render_template('chooseGroup.html',result = choice, message = message)
                else:
                    addition = CourseTeamStudent(rid,currentStudent.CourseId,group,currentStudent.studentID,currentStudent.sectionNo)
                    db.session.add(addition)
                    db.session.commit()
                    number = Member.query.count()
                    addition2 = Member(number+1,currentStudent.studentID,currentStudent.CourseId,currentStudent.sectionNo,1.0,group,'',1)
                    db.session.add(addition2)
                    db.session.commit()
                    message = 'You have chosen group %d!'%(int(group))
                    return render_template('chooseGroup.html',result = choice, message = message)

@divideInBP.route('/redoCG', methods=['GET','POST'])
def redoCG():
    if request.method == 'GET':
        if userPublic.username == '' or userPublic.usertype == 'teacher':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            result = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==currentStudent.CourseId,CourseTeamStudent.StudentID==currentStudent.studentID)).first()
            db.session.delete(result)
            db.session.commit()
            return redirect('./chooseGroup')
    else:
        pass 

@divideInBP.route('/viewresult', methods=['GET','POST'])
def viewresult():
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'teacher':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            tcheck = Course_teacher.query.filter(and_(Course_teacher.CourseId==currentStudent.CourseId,Course_teacher.sectionNo==currentStudent.sectionNo)).first()
            check11 = DivideIn.query.filter(and_(DivideIn.CourseId==currentStudent.CourseId,DivideIn.staffID==tcheck.staffID)).first()
            
            
            result = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==currentStudent.CourseId,CourseTeamStudent.StudentID==currentStudent.studentID)).first()
            if result:
                result1 = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId == currentStudent.CourseId,CourseTeamStudent.sectionNo==currentStudent.sectionNo)).order_by(CourseTeamStudent.Tid).all()
                print('result1')
                print(result1)
                print(currentStudent.CourseId)
                print(currentStudent.sectionNo)
                feed = []
                for i in result1:
                    msg = []
                    msg.append(i.CourseId)
                    msg.append(i.Tid)
                    msg.append(i.StudentID)
                    feed.append(msg)
                return render_template('displaymethod2.html', message = message,result = feed)
            else:
                if check11.methodNo==3:
                    message = 'Groups result has not come out yet'
                    return render_template('stuprompt.html',message=message)
                return redirect('./chooseGroup')
    else:
        pass    

@divideInBP.route('/invite', methods=['GET','POST'])#choosefriend.html
def invite():
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'teacher':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            #看这个人有没有选朋友
            check = Invitation.query.filter(and_(Invitation.CourseId==currentStudent.CourseId,Invitation.sectionNo==currentStudent.sectionNo,Invitation.studentID==currentStudent.studentID)).first()
            if check:
                if check.selection == '':#还没有选朋友
                    #把没有选朋友的人选出来当作可选list
                    selectresult = Course_student.query.filter(and_(Invitation.CourseId==currentStudent.CourseId,Invitation.sectionNo==currentStudent.sectionNo,Invitation.selection=='')).all()
                    result = []
                    result.append('to be alone')#选择不要朋友
                    for i in selectresult:
                        result.append(i.studentID)
                    
                else:#已经选了朋友或者已经有朋友了
                    result = []
                    message = 'You have already select your friend. Please wait for you friend to confirm your invitaion or you could view the group result or redo your choice!'
            else:
                selectresult = Invitation.query.filter(and_(Invitation.CourseId==currentStudent.CourseId,Invitation.sectionNo==currentStudent.sectionNo,Invitation.selection=='')).all()
                result = []
                result.append('to be alone')#选择不要朋友
                for i in selectresult:
                    result.append(i.studentID)

            if result is None or len(result) is 0:
                result=['undecided']      
            else:
                pass
            return render_template('choosefriend.html',result = result,message = message)
    else:
        friend = request.form.get('option')#studentid
        if friend == 'to be alone':
            result = Invitation.query.filter(and_(Invitation.CourseId==currentStudent.CourseId,Invitation.studentID==currentStudent.studentID)).first()
            result.selection = friend
            result.confirm = 1
            db.session.commit()
            message = 'You have chosen to work alone!'
        else:
            result = Invitation.query.filter(and_(Invitation.CourseId==currentStudent.CourseId,Invitation.studentID==currentStudent.studentID)).first()
            result.selection = friend
            db.session.commit()
            message = 'you have sent your invitation to %s successfully!'%friend
        result = []
        if result is None or len(result) is 0:
                result=['undecided']      
        else:
            pass
        return render_template('choosefriend.html',result = result, message = message)

@divideInBP.route('/viewinvitation', methods=['GET','POST'])#viewinvitation.html
def viewinvitation():
    if request.method == 'GET':
        if userPublic.username == '' or userPublic.usertype == 'teacher':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            check = Invitation.query.filter(and_(Invitation.CourseId==currentStudent.CourseId,Invitation.sectionNo==currentStudent.sectionNo,Invitation.studentID==currentStudent.studentID)).first()
            print('checkinvitation')
            print(check)
            if check:#当前用户
                
                if check.selection == '':#还没有选朋友
                    namelist = Invitation.query.filter(and_(Invitation.CourseId==currentStudent.CourseId,Invitation.selection==currentStudent.studentID)).all()
                    if namelist:
                        message = 'You have friend invitations from students in the select list: '
                        result = []
                        for i in namelist:
                            result.append(i.studentID)
            
                    else:
                        message = 'you have not recieved any invitation yet'
                        result = []
                
                else:
                    message = '''You have already chosen a friend, if you want to accept others' invitation, please first click redo to remove your choice!'''
                    result = []
                if result is None or len(result) is 0:
                        result=['undecided']      
                else:
                    pass
                return render_template('viewinvitation.html',result = result, message = message)
            else:
                result = []
                if result is None or len(result) is 0:
                        result=['undecided']      
                else:
                    pass
                message = 'you are not found in this course'
                return render_template('viewinvitation.html',result = result, message = message)
    else:
        friend = request.form.get('option')#studentid
        result = Invitation.query.filter(and_(Invitation.CourseId==currentStudent.CourseId,Invitation.studentID==currentStudent.studentID)).first()
        result.selection = friend
        result.confirm=1
        db.session.commit()
        result = Invitation.query.filter(and_(Invitation.CourseId==currentStudent.CourseId,Invitation.studentID==friend)).first()
        result.confirm=1
        db.session.commit()
        message = 'you have accepted invitation from %s successfully!'%friend
        result = []
        if result is None or len(result) is 0:
                result=['undecided']      
        else:
            pass
        return render_template('viewinvitation.html',result = result, message = message)


@divideInBP.route('/friendRedo', methods=['GET','POST'])
def friendRedo():
    if request.method == 'GET':
        if userPublic.username == '' or userPublic.usertype == 'teacher':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            result = Invitation.query.filter(and_(Invitation.CourseId==currentStudent.CourseId,Invitation.studentID==currentStudent.studentID)).first()
            result2 = Invitation.query.filter(and_(Invitation.CourseId==currentStudent.CourseId,Invitation.studentID==result.selection)).first()
            result.selection = ''
            result.confirm = 0
            db.session.commit()
            result2.confirm = 0
            db.session.commit()
            check = Member.query.filter(and_(Member.CourseId==currentStudent.CourseId,Member.sectionNo==currentStudent.sectionNo)).all()
            if check:
                for i in check:
                    db.session.delete(i)
                    db.session.commit()
            return redirect('./studentGroup')
    else:
        pass

@divideInBP.route('/method3', methods=['GET','POST'])
def method3():
    if request.method == 'GET':
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            result = DivideIn.query.filter(and_(DivideIn.CourseId == currentCourse.CourseId,DivideIn.staffID==currentCourse.staffID)).first()
            result.methodNo = 3
            db.session.commit()
            
            result = Course_teacher.query.filter(and_(Course_teacher.CourseId == currentCourse.CourseId,Course_teacher.sectionNo==currentCourse.sectionNo)).first()
            idstaff = result.staffID
            result1 = DivideIn.query.filter(and_(DivideIn.CourseId==currentCourse.CourseId,DivideIn.staffID==idstaff)).first()
            division.totalGroup = result1.totalGroup
            division.rest = result1.rest
            division.numberPergroup = result1.numberPergroup
            division.totalStu = result1.totalStu
            division.groupNNormal = result1.groupNNormal

            result = Course_teacher.query.filter(and_(Course_teacher.CourseId == currentCourse.CourseId,Course_teacher.sectionNo==currentCourse.sectionNo)).first()
            idstaff = result.staffID
            result1 = DivideIn.query.filter(and_(DivideIn.CourseId==currentCourse.CourseId,DivideIn.staffID==idstaff)).first()
            if int(result1.numberPergroup)%2!=0:
                db.session.delete(result1)
                db.session.commit()
                message = 'The number of members in each group should be even! Your form group decision would be deleted!'
                return render_template('warning.html',message = message)
            else:
                division.totalGroup = result1.totalGroup
                division.rest = result1.rest
                division.numberPergroup = result1.numberPergroup
                division.totalStu = result1.totalStu
                division.groupNNormal = result1.groupNNormal

                #在使用RandNumber之前先清空
                count= RandNumber.query.count()
                if count!=0:   
                    print(type(count))
                    print(count)
                    for i in range(0,count):
                        obj = RandNumber.query.filter(RandNumber.listid==i+1).first()
                        db.session.delete(obj)
                        db.session.commit()
                #使用RandNumber表格
                if int(division.rest)==0:
                
                #每个数字随机生成numberPergroup个
                    while(RandNumber.query.count()<division.totalStu):
                        
                        num = random.randint(1,division.totalGroup)
                        result = RandNumber.query.filter(RandNumber.num==num).count()
                        if result < int(division.numberPergroup):
                            writein = RandNumber(RandNumber.query.count()+1,num)
                            db.session.add(writein)
                            db.session.commit()
                        else:
                            continue

                else:
                    if int(division.totalStu)//int(division.numberPergroup) < int(division.totalGroup):
                        #一个组的人数不同于其他组
                        full = []
                        while(RandNumber.query.count()<division.totalStu):
                        
                            num = random.randint(1,division.totalGroup)#生成随机数
                            result = RandNumber.query.filter(RandNumber.num==num).count()#数现在跟这个随机数相等的有几个
                            if  len(full)<1:
                                if result < int(division.groupNNormal): 
                                    writein = RandNumber(RandNumber.query.count()+1,num)
                                    db.session.add(writein)
                                    db.session.commit()
                                    result = RandNumber.query.filter(RandNumber.num==num).count()
                                    if result == int(division.groupNNormal):
                                        full.append(num)
                                    else:
                                        continue
                                else:
                                    continue
                            else:
                                if result < int(division.numberPergroup):
                                    writein = RandNumber(RandNumber.query.count()+1,num)
                                    db.session.add(writein)
                                    db.session.commit()
                                else:
                                    continue
                                
                                
                    elif int(division.totalStu)//int(division.numberPergroup) == int(division.totalGroup):
                        full = []
                        while(RandNumber.query.count()<division.totalStu):
                            num = random.randint(1,division.totalGroup)#随机组数
                            result = RandNumber.query.filter(RandNumber.num==num).count()#这个组数的数量
                            #组数等于groupNNormal而且等于groupNNormal的组的数量不到rest个
                            if len(full)<int(division.rest):
                                if result < int(division.groupNNormal):
                                    writein = RandNumber(RandNumber.query.count()+1,num)
                                    db.session.add(writein)
                                    db.session.commit()
                                    result = RandNumber.query.filter(RandNumber.num==num).count()
                                    if result == int(division.groupNNormal):
                                        full.append(num)
                                    else:
                                        continue
                                else:
                                    continue
                            else:
                                if result<int(division.numberPergroup):
                                    writein = RandNumber(RandNumber.query.count()+1,num)
                                    db.session.add(writein)
                                    db.session.commit()
                                else:
                                    continue
            result = RandNumber.query.all()
            #把结果写进courseteamstudent的数据库里面
            sectionresult = Course_teacher.query.filter(and_(Course_teacher.staffID == division.staffID,Course_teacher.CourseId == division.CourseId)).first()
            section = sectionresult.sectionNo
            
            allresult = Course_student.query.filter(and_(Course_student.CourseId == division.CourseId,Course_student.sectionNo==section)).first()
            iiid = allresult.rrrid
            
            for i in result:
                count = CourseTeamStudent.query.count()
                alresult = Course_student.query.filter(Course_student.rrrid == iiid).first()
                iiid = int(iiid)+1
                result = CourseTeamStudent(rid=count+1,CourseId = division.CourseId,Tid=i.num, StudentID = '', sectionNo = currentCourse.sectionNo)
                db.session.add(result)
                db.session.commit()
            #删除随机数的数据库
            num = RandNumber.query.count()
            print(type(num))
            print(num)
            for i in range(0,num):
                obj = RandNumber.query.filter(RandNumber.listid==i+1).first()
                db.session.delete(obj)
                db.session.commit()
            
            message = 'Waiting for students to choose their friends. Only pairs information is complete, could the form group process started!'
        return render_template('warning.html',message = message)
    else:
        pass

@divideInBP.route('/formGroup', methods=['GET','POST'])
def formGroup():
    if request.method == 'GET':
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            check = Invitation.query.filter(and_(Invitation.CourseId==currentCourse.CourseId,Invitation.sectionNo==currentCourse.sectionNo,Invitation.confirm==0)).first()
            if check:
                message = '''Students' choosing friends process is not over yet. The form group could start after the data is complete!'''
            else:
                message = 'data is now complete and the form group process could start now!'
            return render_template('formGroup.html',message = message)
    else:
        check = Invitation.query.filter(and_(Invitation.CourseId==currentCourse.CourseId,Invitation.sectionNo==currentCourse.sectionNo,Invitation.confirm==0)).first()
        if check:
            message = '''Students' choosing friends process is not over yet. The form group could start after the data is complete!'''
            return render_template('formGroup.html',message = message)
        else:
            
            result = Course_teacher.query.filter(and_(Course_teacher.CourseId == currentCourse.CourseId,Course_teacher.sectionNo==currentCourse.sectionNo)).first()
            idstaff = result.staffID
            result1 = DivideIn.query.filter(and_(DivideIn.CourseId==currentCourse.CourseId,DivideIn.staffID==idstaff)).first()
            division.totalGroup = result1.totalGroup
            division.rest = result1.rest
            division.numberPergroup = result1.numberPergroup
            division.totalStu = result1.totalStu
            division.groupNNormal = result1.groupNNormal

            total = Invitation.query.filter(and_(Invitation.CourseId==currentCourse.CourseId,Invitation.sectionNo==currentCourse.sectionNo)).count()
            count = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==currentCourse.CourseId,CourseTeamStudent.sectionNo==currentCourse.sectionNo,CourseTeamStudent.StudentID=='')).count()
            opresult = Invitation.query.filter(and_(Invitation.CourseId==currentCourse.CourseId,Invitation.sectionNo==currentCourse.sectionNo)).first()
            op = opresult.iid #这个班invitation开始的iid
            print('opop')
            print(op)
            end = total+op-2 #这个班的最后一个iid
            print('total')
            print(total)
            #从courseteamstudent里面选第一个tid出来
            first = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==currentCourse.CourseId,CourseTeamStudent.sectionNo==currentCourse.sectionNo)).first()
            firstid = first.rid#这个课名单开始的序号
            first = CourseTeamStudent.query.filter(CourseTeamStudent.rid==firstid).first()#找到courseTeamStudent相应course的第一个
            nid = first.Tid#第一个tid
            #------------------------------------------------------------------------------------------------------------------------
            while(count!=0):
                print('count')
                print(count)
                #从CTS里选一个tid，第一个tid
                
                #这个tid有多少个空位
                empty = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==currentCourse.CourseId,CourseTeamStudent.sectionNo==currentCourse.sectionNo,CourseTeamStudent.StudentID=='',CourseTeamStudent.Tid==nid)).count()
                #如果空位大于两个
                inter = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==currentCourse.CourseId,CourseTeamStudent.sectionNo==currentCourse.sectionNo,CourseTeamStudent.StudentID=='',CourseTeamStudent.Tid==nid)).first()
                if empty>=2:
                    
                    
                    #从invitation里面挑第一对同学
                    select = Invitation.query.filter(and_(Invitation.CourseId==currentCourse.CourseId,Invitation.sectionNo==currentCourse.sectionNo,Invitation.iid ==op)).first()
                    if select.selection =='to be alone':
                        print('I am here11')
                        #找到第一个有空位的
                        next = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==currentCourse.CourseId,CourseTeamStudent.sectionNo==currentCourse.sectionNo,CourseTeamStudent.StudentID=='')).first()
                        #nextid = next.rid
                        nid = next.Tid
                        continue
                    else:
                        print('I am here22')
                        
                        inter.StudentID=select.studentID
                        print(inter.StudentID)
                        print(select.studentID)
                        db.session.commit()
                        s2 = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==currentCourse.CourseId,CourseTeamStudent.sectionNo==currentCourse.sectionNo,CourseTeamStudent.StudentID=='',CourseTeamStudent.Tid==nid)).first()
                        s2.StudentID = select.selection
                        db.session.commit()
                        op = op+1
                        next = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==currentCourse.CourseId,CourseTeamStudent.sectionNo==currentCourse.sectionNo,CourseTeamStudent.StudentID=='')).first()
                        if next:
                            nextid = next.rid
                            nid = next.Tid
                        else:
                            pass
                        find = Invitation.query.filter(and_(Invitation.CourseId==currentCourse.CourseId,Invitation.sectionNo==currentCourse.sectionNo,Invitation.studentID==select.selection,Invitation.selection==select.studentID)).first()
                        db.session.delete(find)
                        db.session.commit()
                        db.session.delete(select)
                        db.session.commit()
                elif empty==1:
                    print('I am here33')
                    select = Invitation.query.filter(and_(Invitation.CourseId==currentCourse.CourseId,Invitation.sectionNo==currentCourse.sectionNo,Invitation.selection =='to be alone')).first()
                    inter.StudentID = select.studentID
                    db.session.commit()
                    next = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==currentCourse.CourseId,CourseTeamStudent.sectionNo==currentCourse.sectionNo,CourseTeamStudent.StudentID=='')).first()
                    if next:
                        nextid = next.rid
                        nid = next.Tid
                    else:
                        pass
                    check = Invitation.query.filter(and_(Invitation.CourseId==currentCourse.CourseId,Invitation.sectionNo==currentCourse.sectionNo)).first()
                    op = check.iid
                else:
                    break
                    next = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==currentCourse.CourseId,CourseTeamStudent.sectionNo==currentCourse.sectionNo,CourseTeamStudent.StudentID=='')).first()
                    nextid = next.rid
                    nid = next.Tid
                    print('I am here44')
                    continue 
            #---------------------------------------------------------------------------------------------------------------------------    
            
            select = CourseTeamStudent.query.filter(and_(CourseTeamStudent.CourseId==currentCourse.CourseId,CourseTeamStudent.sectionNo==currentCourse.sectionNo)).all()
            for i in select:
                number = Member.query.count()
                result = Member(number+1,i.StudentID,i.CourseId,i.sectionNo,1.0,i.Tid,'',1)
                db.session.add(result)
                db.session.commit()
            return redirect('./showresult')
                