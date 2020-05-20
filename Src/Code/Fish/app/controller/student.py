from flask import Blueprint,render_template, request, redirect
from app.models.base import db
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.course import Course
from app.models.course_teacher import Course_teacher
from app.models.course_student import Course_student
from app.models.invitation import Invitation
from app.models.user import User,userPublic
from sqlalchemy import or_,and_,all_,any_
from flask.helpers import url_for


studentBP = Blueprint('student',__name__)

@studentBP.route('/mainPage',methods=['GET','POST'])
def main_page():
    if request.method == 'GET' :
        if userPublic.username == '' or userPublic.usertype == 'teacher':
            print (userPublic.username)
            print('\n')
            return redirect('http://127.0.0.1:5000/user/login')
        else:
            print (userPublic.username)
            print('\n')
        return render_template('student.html')
    else:
        pass

@studentBP.route('/setInfo', methods=['GET','POST'])
def setInfo():
    if request.method == 'GET' :
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
        return render_template('importindividual.html',result = result)
      
    else:
        namecourse = request.form.get('option')
        StudentID = request.form.get('studentID')
        studentname = request.form.get('studentname')
        GPA = request.form.get('exampleInputGPA1')
        Email = request.form.get('exampleInputEmail1')
        result = Course.query.filter(Course.CourseName==namecourse).first()
        idcourse = result.CourseId
        #GPA 在网页上要设一个defaut的value
        print(StudentID, studentname, GPA, Email)
        result1 = Course_teacher.query.filter(Course_teacher.CourseId==result.CourseId).first()
        section = result1.sectionNo
        result = Course_student.query.filter(and_(Course_student.studentID==StudentID,Course_student.CourseId==idcourse)).first()
        if result:
            result2 = Invitation.query.filter(and_(Invitation.CourseId==idcourse,Invitation.studentID==StudentID)).first()
            if result2:
                pass
            else:
                count = Invitation.query.count()
                iid = count+1
                add = Invitation(iid,idcourse,section,StudentID,'',0)
                db.session.add(add)
                db.session.commit()
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
            message = 'student %s is already in this course'%(studentname)
            return render_template('importindividual.html',message = message,result = result)
        else:
            count = Course_student.query.count()
            rrrid = count+1
            addition = Course_student(rrrid,StudentID,idcourse,section)
            db.session.add(addition)
            db.session.commit()
            result1 = Student.query.filter(Student.StudentID==StudentID).first()
            result2 = Invitation.query.filter(and_(Invitation.CourseId==idcourse,Invitation.studentID==StudentID)).first()
            if result2:
                pass
            else:
                count = Invitation.query.count()
                iid = count+1
                add = Invitation(iid,idcourse,section,StudentID,'',0)
                db.session.add(add)
                db.session.commit()
            if result1:
                pass
            else:
                result = Student(StudentID,studentname, Email,GPA)
                #往student的数据库表格中插入数据
                db.session.add(result)
                db.session.commit()
                #往User的数据库表格中插入数据并生成初始密码
            check = User.query.filter(User.username==Email).first()
            if check:
                pass
            else:
                result1 = User(Email, '123456','student')
                db.session.add(result1)
                db.session.commit()

           
            message = 'information record successfully'
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
            return render_template('importindividual.html',message = message,result = result)
            
        

