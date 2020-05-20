from flask import Blueprint,render_template, request
from app.models.base import db
from app.models.randNumber import RandNumber

randNumberBP = Blueprint('randNumber',__name__)

@randNumberBP.route('', methods=['GET'])
def get_leader():
    with RandNumber.auto_commit():
        randNumber = RandNumber("1730026000", 'ACHN0763', 4.0, 5.0)
        # 数据库的insert操作
        RandNumber.session.add(randNumber)
    
    return 'hello leader'
