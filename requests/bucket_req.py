from datetime import datetime
import models.bucket_models as bm
from app import db


tusr = bm.TblUser
tws = bm.TblWish


def check_user(usr_name):
    _name = db.session.query(tusr).filter(tusr.user_name == usr_name).all()
    if len(_name) == 0:
        return None
    else:
        return _name[0].user_name


def get_user(email):
    _name = db.session.query(tusr).filter(tusr.user_username == email).all()
    if len(_name) == 0:
        return None
    else:
        return _name[0]


def create_user(name, email, pwd):
    try:
        new_user = tusr(user_name=name,
                        user_username=email,
                        user_password=pwd)
        db.session.add(new_user)
        db.session.commit()
    except Exception as ex:
        return str(ex)


def create_wish(title, description, user):
    try:
        new_wish = tws(wish_title=title,
                       wish_description=description,
                       wish_user_id=user,
                       wish_date=datetime.now())
        db.session.add(new_wish)
        db.session.commit()
        return True
    except Exception as ex:
        return False


def get_wish_by_user(user):
    uids = db.session.query(tws).filter(tws.wish_user_id == user).all()
    if len(uids) == 0:
        return None
    else:
        return uids


def get_wish_pagination_by_user(user_id, limit, offset):
    uids = db.session.query(tws).filter(tws.wish_user_id == user_id).order_by(tws.wish_id)
    uids = uids.limit(limit)
    uids = uids.offset(offset)
    return uids.all()


def get_count_wish(user):
    return db.session.query(tws).filter(tws.wish_user_id == user).count()


def get_wish_by_id(wish_id, user):
    wish = db.session.query(tws).filter(tws.wish_id == wish_id,
                                        tws.wish_user_id == user).all()
    if len(wish) == 0:
        return None
    else:
        return wish[0]


def update_wish(title, description, wish_id, user):
    try:
        db.session.query(tws).filter(
            tws.wish_id == wish_id,
            tws.wish_user_id == user)\
            .update({
              tws.wish_title: title,
              tws.wish_description: description
            })

        db.session.commit()
        return True
    except Exception:
        return False


def delete_wish(wish_id, user):
    try:
        db.session.query(tws).filter(
            tws.wish_id == wish_id,
            tws.wish_user_id == user)\
            .delete()
        db.session.commit()
        return True
    except Exception:
        return False
