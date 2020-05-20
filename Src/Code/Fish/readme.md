
## Resource

* [Flask1.0+](https://flask.palletsprojects.com/en/1.1.x/)
* [SQLAlchemy](https://www.sqlalchemy.org/)

---

## library

```py
pip install Flask PyMySQL SQLAlchemy Flask-SQLAlchemy xlrd xlwt urllib 
```

---

# Something before testing

1. secure.py  update your own db

2. app -> __init__.py   update blueprint

3. In controller/files.py line 219, please change into where you want to store the export.xls

4. All the information for students, teachers, and courses are randomly formed to get a better test. As can be see in the *data* folder of *files* folder

5. Open the XAMPP, import the **ws3.sql** in *files* folder to form a database with some basic data.

> Now, you get the only user as a teacher for testing.
> Teacher account:
> Kxcjkuzfv@uic.edu.hk
> password:
> 123456

---

If you want to do that by yourself then do the following
- Open the XAMPP, create a database name 'ws3' then run the teamwork.py to build the tables
- Import the testing data in the *files* folder
    - course_teacher.csv into the table course_teacher 
    - course.csv into the table course
    - teacher.csv into the table teacher
    - user.csv into the table user

---

## To test the system

### Login
- Use the account above to login as a teacher. 
- Students account will be considered to be given by the teacher offline out of the system. Here you can go to the database *user* table to get one or import one you like.

### Import 
#### Import the whole class
- teacher main page -> import -> class, and select the first course as example, whose name is 'zlspxykft', and import the file named 'DLJF0718.xls' in the *files* folder. 
#### Import the those late students
- teacher main page -> import -> individual student, and import the new student account into the first course 'zlspxykft' as example.
 - The same account can not be joined again

### Change course name
- teacher main page -> modify course name, change course name is always available for you.
~~Due to the user type, we think it's strange to allow all the teachers changing to course name freely so we skip this function in our demo time this morning~~

### Edit submission items
- teacher main page -> edit items, add / modify / delete of the items are available. 

### Form groups
- teacher main page -> form groups, three methods are available. The system will provide 2 advice when you are going to form groups with a group number cannot be divisible. And you can always redo your choice. 
 - By system
 - By students
 - By system and students
- After the forming group result is completed, functions in student main page would have the data to test.
- To be honest, we didn't finish the way for considering GPA when works done by system. We didn't find the  exact requirement about how to divide the students according to GPA. Sorry about that.
~~Actually, we think it's quite unpleasant for students to be divided by this. It seems that it's not good for the motivation for students.~~

### Change password
- student main page -> change password, logout automatically when successfully changed. 

### Group function
- You can redo whenever you kick the redo button.
#### See the result [Teacher choose to form by system]
- student main page -> group, after selected the course you can see.
#### Join groups [Teacher choose to form by student]
- student main page -> group, after selected the course you can choose your group.
- **please make sure all students are in their groups before testing the student functions except 'group' and 'change password' in the student main page.
- Then go back to the teacher's function to finish the grouping.
#### Invite friends [Teacher choose to form by system and student]
- student main page -> group, after selected the course you can invite your friend.
- You can see the invitations from your friends as well, and accept and reject them.
- Student invite system would only open after teacher select to form group by both system and students.
- **After sending the invitation, please check the invitation table in the database. If in the invitation one studentID is empty, please import the class information into the database again. It is because the database goes wrong.**
- For testing, the method form by system and student actually contain the above 2 methods. And we create a random invitation table among the students. 
- Please empty the invitation table in the database and import 'invitation.csv' in the *files* folder into the invitation table. Then the form group process would be ready. 
- Then go back to the teacher's function to finish the grouping.

### Vote Leader
- **Please make sure the grouping is finished already, no matter what method has been chosen.**
- student main page -> vote leader, student you do that and see the result. 

### Evaluate Leader
- **Please make sure the grouping is finished already, no matter what method has been chosen.**
- **You can only do that if you are a member.**
- student main page -> evaluate leader, then you can do that. 
- To be honest, you can do that a lot of times. 

### Evaluate Member
- **Please make sure the grouping is finished already, no matter what method has been chosen.**
- **You can only do that if you are a leader.**
- student main page -> evaluate member, then you can do that. 
- To be honest, you can do that a lot of times. 

### Export
- teacher main page -> export, Please! 
- **In controller/files.py line 219, please change into where you want to store the export.xls**

---

## Notice!
You can not visit the sites by changing the address even through you login already. 
Like after a student logined, he tries to jump to the teacher site, which is not allowed. 

---

## More to add
GitHub is really useful if we have VPN! I enjoy it a lot in another course. 
But due to the connection problem, we decided to use WeChat directly in this project~

If there is any problems in testing, please contact Winnie(m730026106@mail.uic.edu.hk). 

Thank you so much!!!

Best Wishes,
Fish