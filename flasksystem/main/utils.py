from flask_login import current_user
from flask import abort

def check_lab():
    if current_user.area != 'Lab' and current_user.area != 'Lab_Bod':
        return abort(403)

def check_bod():
    if current_user.area != 'Bod' and current_user.area != 'Lab_Bod':
        return abort(403)

def check_only_lab():
    if current_user.area != 'Lab':
        return abort(403)

def check_only_bod():
    if current_user.area != 'Bod':
        return abort(403)