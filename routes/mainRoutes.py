from flask import Blueprint, render_template
from flask_login import login_required, current_user
import databases.models as models
from databases.models.user import AccessRoleEnum

#Blueprint to define the home page 
main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=['GET', 'POST'])
@login_required
def home():
    username= current_user.username
    user= models.User.query.filter_by(username=username).first()    
    return render_template("index.html", firstName=user.firstName,  AccessRoleEnum=AccessRoleEnum)
