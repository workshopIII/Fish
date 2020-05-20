from flask import Blueprint,render_template, request
from app.models.base import db
from app.models.invitation import Invitation

invitationBP = Blueprint('invitation',__name__)

@invitationBP.route('', methods=['GET'])
def get_invitation():
    with db.auto_commit():
        invitation = Invitation()
        invitation.TeamName = 'g1'
        invitation.TeamNumber = 0
        # 数据库的insert操作
        db.session.add(invitation)
    
    return 'hello team'