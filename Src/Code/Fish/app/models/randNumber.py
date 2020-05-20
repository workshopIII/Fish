from sqlalchemy import Column, String, Integer, orm, ForeignKey
from app.models.base import Base


class RandNumber(Base):
    __tablename__ = 'randNumber'
    listid = Column(Integer,primary_key=True,nullable=False)
    num = Column(Integer)


    def __init__(self, listid, num):
        super(RandNumber,self).__init__()
        self.listid = listid
        self.num = num
    
    def jsonstr(self):

        jsondata = {
            'listid':self.listid,
            'num': self.num,
            
        }
        return jsondata

