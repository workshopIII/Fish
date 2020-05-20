from flask import Blueprint,render_template, request, redirect
from app.models.base import db
from app.models.subItem import SubItem
from app.models.user import User, userPublic
from app.models.subItem import SubItem,currentSub
from app.models.teacher import Teacher,teacherPublic
from app.models.course import Course
from app.models.course_teacher import Course_teacher,currentCourse
from app.models.course_student import Course_student
from app.models.CourseTeamStudent import CourseTeamStudent
from sqlalchemy.sql import text
import pymysql
from wtforms.fields import simple
from sqlalchemy import or_,and_,all_,any_
from app.models.divideIn import DivideIn,division

subItemBP = Blueprint('subItem',__name__)

@subItemBP.route('/selectCourse', methods=['GET','POST'])
def selectCourse():
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'student':
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            result = Teacher.query.filter(Teacher.email == userPublic.username).first()
            result = result.staffid
            division.staffID = result
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
            return render_template('selectCourse.html', result = result, message = message)
    else:
        namecourse = request.form.get('option')
        result = Course.query.filter(Course.CourseName==namecourse).first()
        currentCourse.CourseId = result.CourseId
        currentSub.CourseId = result.CourseId
        division.CourseId = result.CourseId
        result = Course_teacher.query.filter(Course_teacher.CourseId==currentCourse.CourseId).first()
        currentCourse.sectionNo = result.sectionNo
        currentSub.sectionNo = result.sectionNo
        return redirect('./checkPercentage')

@subItemBP.route('/checkPercentage', methods=['GET','POST'])
def checkPercentage():
    if request.method == 'GET':
        message = ''
        percentage = 0
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            result = SubItem.query.filter(SubItem.CourseId == currentCourse.CourseId).all()
            if result is None:
                percentage = 0
            else:
                for i in result:
                    percentage += i.percentage
            if percentage != 100:
                message = 'The percentage is not equal to 100 yet, please keep adding or editing the submission items.'
            else:
                message = 'The percentage is equal to 100 already, you can save after your final edit.'
            return render_template('edititems.html', percentage = percentage, message = message)

@subItemBP.route('/addOneItem', methods=['GET','POST'])
def addOneItem():
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
        return render_template('addoneitem.html', message = message)
    else:
        title = request.form.get('Title')
        percentage = request.form.get('Percentage')
        if title == '' or percentage == '':
            message = 'You must filled all the blanks!'
            return render_template('addoneitem.html', message = message)
        elif int(percentage) <= 0 or int(percentage) >= 100:
            message = 'The percentage should be in the range of (0,100)!'
            return render_template('addoneitem.html', message = message)
        else:
            check = SubItem.query.count()
            if check == 0:
                insert = SubItem(1, title, percentage, currentCourse.CourseId, currentCourse.sectionNo)
                db.session.add(insert)
                db.session.commit()
                message = 'Created!!'
                return render_template('addoneitem.html', message = message)
            else:
                sid = SubItem.query.order_by(-SubItem.Sid).first()
                currentSid = sid.Sid + 1
                result = SubItem.query.filter(and_(SubItem.CourseId==currentSub.CourseId,SubItem.sectionNo==currentSub.sectionNo,SubItem.sTitle == title)).first()
                
                if result is None:
                    percentageExisted = 0
                    check = SubItem.query.filter(SubItem.CourseId == currentCourse.CourseId).all()
                    if check is None:
                        percentageExisted = 0
                    else:
                        for i in check:
                            percentageExisted += i.percentage
                    newp = percentageExisted + int(percentage)
                    print('newp')
                    print(newp)
                    if  newp <= 100:
                        insert = SubItem(currentSid, title, percentage, currentCourse.CourseId, currentCourse.sectionNo)
                        db.session.add(insert)
                        db.session.commit()
                        message = 'Created!!'
                        return render_template('addoneitem.html', message = message)
                    else:
                        message = 'Failed! The total percentage is bigger than 100!!'
                        return render_template('addoneitem.html', message = message)
                else:
                    message = 'The item already existed!!'
                    return render_template('addoneitem.html', message = message)


@subItemBP.route('/editoneitem', methods=['GET','POST'])
def editOneItem():
    if request.method == 'GET':
        message = ''
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            getr = SubItem.query.filter(and_(SubItem.CourseId==currentCourse.CourseId,SubItem.sectionNo==currentCourse.sectionNo)).all()
            if getr:
                feed = []
                for i in getr:
                    feed.append(i.sTitle)
            else:
                pass
            if feed is None or len(feed) is 0:
                feed=['undecided']      
            else:
                pass
        return render_template('editoneitem.html', message = message,result = feed)
    else:
        title = request.form.get('option')
        percentage = request.form.get('Percentage')
        if title == '' or percentage == '':
            message = 'You must filled all the blanks!'
            return render_template('editoneitem.html', message = message)
        elif int(percentage) <= 0 or int(percentage) >= 100:
            message = 'The percentage should be in the range of (0,100)!'
            return render_template('editoneitem.html', message = message)
        else:
            result = SubItem.query.filter(and_(SubItem.CourseId==currentSub.CourseId,SubItem.sectionNo==currentSub.sectionNo,SubItem.sTitle == title)).first()
            currentSub.percentage =result.percentage
            if result is None:
                message = 'The item does not existed!!'
                return render_template('editoneitem.html', message = message)
            else:
                percentageExisted = 0
                check = SubItem.query.filter(SubItem.CourseId == currentCourse.CourseId).all()
                if check is None:
                    percentageExisted = 0
                else:
                    for i in check:
                        percentageExisted += i.percentage
                newp = percentageExisted - int(currentSub.percentage) + int(percentage)
                print('newp')
                print(newp)
                    
                if  newp <= 100:
                    result.percentage = percentage
                    db.session.commit()
                    message = 'Changed!!'
                else:
                    message = 'Failed! The total percentage is bigger than 100!!'
                getr = SubItem.query.filter(and_(SubItem.CourseId==currentCourse.CourseId,SubItem.sectionNo==currentCourse.sectionNo)).all()
                if getr:
                    feed = []
                    for i in getr:
                        feed.append(i.sTitle)
                else:
                    pass
                if feed is None or len(feed) is 0:
                    feed=['undecided']      
                else:
                    pass
                return render_template('editoneitem.html', message = message,result = feed)

@subItemBP.route('/deleteOneItem', methods=['GET','POST'])
def deleteOneItem():
    if request.method == 'GET':
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            getr = SubItem.query.filter(and_(SubItem.CourseId==currentCourse.CourseId,SubItem.sectionNo==currentCourse.sectionNo)).all()
            if getr:
                feed = []
                for i in getr:
                    feed.append(i.sTitle)
            else:
                pass
            if feed is None or len(feed) is 0:
                feed=['undecided']      
            else:
                pass
            return render_template('deleteoneitem.html',result=feed)
    else:
        title = request.form.get('option')
        if title == '':
            message = 'You must filled all the blanks!'
        else:
            result = SubItem.query.filter(SubItem.sTitle == title).first()
            if result is None:
                message = 'The item does not existed!!'
            
            else:
                sid = result.Sid
                delete = SubItem.query.filter(SubItem.Sid == sid).first()
                db.session.delete(delete)
                db.session.commit()
                message = 'Deleted!!'
            getr = SubItem.query.filter(and_(SubItem.CourseId==currentCourse.CourseId,SubItem.sectionNo==currentCourse.sectionNo)).all()
            if getr:
                feed = []
                for i in getr:
                    feed.append(i.sTitle)
            else:
                pass
            if feed is None or len(feed) is 0:
                feed=['undecided']      
            else:
                pass
            return render_template('deleteoneitem.html', message = message,result = feed)

@subItemBP.route('/save', methods=['GET','POST'])
def save():
    message = ''
    percentage = 0
    if request.method == 'GET':
        if userPublic.username == '' or userPublic.usertype == 'student':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
            result = SubItem.query.filter(SubItem.CourseId == currentCourse.CourseId).all()
            if result is None:
                percentage = 0
            else:
                for i in result:
                    percentage += i.percentage
            if percentage != 100:
                message = 'The percentage is not equal to 100 yet, please keep adding or editing the submission items.'
                return render_template('edititems.html', percentage = percentage, message = message)
            else:
                return render_template('teacher.html')