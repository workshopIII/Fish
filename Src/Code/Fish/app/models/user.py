from sqlalchemy import Column, String, Integer, orm, ForeignKey
from app.models.base import Base


class User(Base):
    __tablename__ = 'user'
    username = Column(String(100),primary_key=True,nullable=False)
    psw = Column(String(50), nullable=False)
    usertype = Column(String(30), nullable=False)


    def __init__(self, username, password, usertype):
        super(User,self).__init__()
        self.username = username
        self.psw = password
        self.usertype  = usertype
    
    def jsonstr(self):

        jsondata = {
            'username':self.username,
            'password': self.psw,
            'usertype': self.usertype,
            
        }
        return jsondata
userPublic = User('','','')

