
import requests
from flask import Flask, render_template, session, redirect, request, jsonify, url_for
from datetime import datetime
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
from hashingcrypt import encrypt, checkpassword
app.secret_key = "ddsdadw"
# app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)


user_group_association_table = db.Table('user_group_association', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')), 
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))    
)

chat_group_association_table = db.Table('chat_group_association',
    db.Column('chat', db.Integer, db.ForeignKey('chat.id')), 
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

chat_user_association_table = db.Table('chat_user_association',
    db.Column('chat', db.Integer, db.ForeignKey('chat.id')), 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

likes_user_association_table = db.Table('likes_user_association',
    db.Column('chat', db.Integer, db.ForeignKey('chat.id')), 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    liked_by = db.relationship("User", secondary=likes_user_association_table, backref="likes")
    chat_by = db.relationship("User", secondary=chat_user_association_table, backref="chats")
    time=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship("User", secondary=user_group_association_table, backref="groups")
    chats = db.relationship("Chat", secondary=chat_group_association_table, backref="groups")

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50), unique=True)
    password=db.Column(db.String(200), nullable=False)
    type=db.Column(db.String(5), nullable=False)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            # print('Requestor: ' + session['requestor'], flush=True)
            return jsonify({'success':False, 'error_msg': "username not found"}) # Authorization required
        else:
            return function(*args, **kwargs)
    wrapper.__name__ = function.__name__
    return wrapper

def admin_required(function):
    def wrapper(*args, **kwargs):
        if "type" not in session or session['type']!='admin':
            # print('Requestor: ' + session['requestor'], flush=True)
            return jsonify({'success':False}) # Authorization required
        else:
            return function(*args, **kwargs)
    wrapper.__name__ = function.__name__
    return wrapper

#API calls
@app.route('/', methods=['GET', 'POST'])
def html_home():
    return jsonify({"message":'Group chat application is running, developed by Anshuman, email: anxumaan@gmail.com'})

#login API
@app.route('/api/v1/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname,pword="",""
        # using HTML Forms
        try:
            data=request.get_json()
            uname=data['username']
            pword=data['password']

        # using application/json request
        except Exception as e:
            print(e)
            return jsonify({'success': False})
        # print(encrypt(password))
        encrypted=encrypt(pword)
        user=User.query.filter_by(username=uname).first()
        if user and checkpassword(pword, user.password):
            session['username']=uname
            session['logged_in']=True
            session['type']=user.type
            # print(session['username'], session['type'], ": logged in", session)
            data = {'success': True, 'username':session['username'], 'logged_in': session['logged_in'], 'type': session['type']}
            return jsonify(data)
        else:
            return jsonify({'success': False})

    return "login API"

#sign up API
@app.route('/api/v1/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        uname,pword="",""
        # using HTML Forms
        try:
            data=request.get_json()
            uname=data['username']
            pword=data['password']
        except Exception as e:
            print(e)
            return jsonify({'success': False})

        try:    
            encrypted=encrypt(pword)
            user=User(username=uname, password=encrypted, type='admin')
            db.session.add(user)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            print(e)
            return jsonify({'success': False})
    return "Signup API"


#API for admin to add/create new users
@app.route('/api/v1/add_user', methods=['GET', 'POST'])
@login_is_required
@admin_required
def add_user():
    if request.method == 'POST':
        #adding normal users with default password
        uname,pword="","password"
        # using HTML Forms
        try:
            if request.form:
                uname=request.form['username']
            else:
                data=request.get_json()
                uname=data['username']

        # using application/json request
        except Exception as e:
            print(e)
            return jsonify({'success': False})

        try:    
            encrypted=encrypt(pword)
            user=User(username=uname, password=encrypted, type='normal')
            db.session.add(user)
            db.session.commit()
            return jsonify({'success': True}) 
        except Exception as e:
            print(e)
            return jsonify({'success': False})
    return "Adding Normal User API"


#API to change password
@app.route('/api/v1/change_password', methods=['GET', 'POST'])
@login_is_required
def change_password():
    if request.method == 'POST':
        uname=session['username']
        pword=""
        # using HTML Forms
        try:
            if request.form:
                pword=request.form['password']
                new_pword=request.form['new_password']
            else:
                data=request.get_json()
                pword=data['password']
                new_pword=data['new_password']

        # using application/json request
        except Exception as e:
            print(e)
            return jsonify({'success': False})

        try:    
            encrypted=encrypt(pword)
            user=User.query.filter_by(username=uname).first()
            if checkpassword(pword, user.password):
                newpwd=encrypt(new_pword)
                user.password=newpwd
                db.session.commit()
                return jsonify({'success': True})
            else:
                return jsonify({'success': False})
        except Exception as e:
            return jsonify({'success': False})
    return "Password Change API"

#API for admins to edit user details
@app.route('/api/v1/edit_user', methods=['GET', 'POST'])
@login_is_required
@admin_required
def edit_user():
    if request.method == 'POST':
        #adding normal users with default password
        uname,pword="",""
        type=""
        try:
            data=request.get_json()
            uname=data['username']
            new_uname=data['new_username']
            pword=data['password']
            type=data['type']
        except Exception as e:
            print(e)
            return jsonify({'success': False})

        try:
            encrypted=encrypt(pword)
            user=User.query.filter_by(username=uname).first()
            user.username=new_uname
            user.password=encrypted
            user.type=type
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False})
    return "Edit User API"

#logout API
@app.route("/api/v1/logout", methods=['GET','POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

#Group APIs for normal user

#Create Groups
@app.route("/api/v1/create_group", methods=['GET','POST'])
@login_is_required
def create_group():
    if request.method == 'POST':
        print("User logged in is ", session['username'])
        #adding normal users with default password
        gname=""
        try:
            data=request.get_json()
            gname=data['groupname']
        # using application/json request
        except Exception as e:
            print(e)
            return jsonify({'success': False})

        try:
            group=Group(name=gname)            
            user=User.query.filter_by(username=session['username']).first()
            print('user: ', user.username)
            group.users.append(user)
            db.session.add(group)
            db.session.commit()
            print("group created: ", group.name)
            return jsonify({'success': True})
        except Exception as e:
            print(e)
            return jsonify({'success': False})

    return "group created"

#Delete Groups
@app.route("/api/v1/delete_group/<id>", methods=['GET','POST'])
@login_is_required
def delete_group(id):
    try:
        user=User.query.filter_by(username=session['username']).first()
        group=Group.query.filter_by(id=int(id)).first()
        if user in group.users:  
            db.session.delete(group)
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})
    except Exception as e:
        print(e)
        return jsonify({'success': False})

#Search Groups
@app.route("/api/v1/search_groups", methods=['GET','POST'])
@login_is_required
def search_groups():
    g=Group.query.all()
    user=User.query.filter_by(username=session['username']).first()
    group_data=[]
    for groups in g:
        if user in groups.users:
            data={
                "group_id": groups.id,
                "groupname":groups.name
            }
            group_data.append(data)
    final_data={'group_data':group_data, 'success': True}
    return jsonify(final_data)

#Add Members to a group
@app.route("/api/v1/add_members/<group_id>/<user_id>", methods=['GET','POST'])
@login_is_required
def add_members(group_id,user_id):
    try:
        user=User.query.filter_by(id=user_id).first()
        group=Group.query.filter_by(id=int(group_id)).first()
        me=User.query.filter_by(username=session['username']).first()
        if me in group.users:
            group.users.append(user)
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})
    except Exception as e:
        print(e)
        return jsonify({'success': False})

#Send Message to a group
@app.route("/api/v1/send_message/<group_id>", methods=['GET','POST'])
@login_is_required
def send_message(group_id):
    if request.method == 'POST':
        message=""
        try:
            data=request.get_json()
            message=data['message']
        except Exception as e:
            print(e)
            return jsonify({'success': False})

        try:    
            group=Group.query.filter_by(id=int(group_id)).first()          
            user=User.query.filter_by(username=session['username']).first()
            print(group.users)
            if user in group.users:
                chat=Chat(message=message)
                # print("Debug")
                group.chats.append(chat)
                chat.chat_by.append(user)
                db.session.add(chat)
                db.session.commit()
                print(group.chats)
            return jsonify({'success': True})
        except Exception as e:
            print(e)
            return jsonify({'success': False})

    return "Sending message"

#like Message
@app.route("/api/v1/like_message/<chat_id>", methods=['GET','POST'])
@login_is_required
def like_message(chat_id):
    try:          
        user=User.query.filter_by(username=session['username']).first()
        chat=Chat.query.filter_by(id=int(chat_id)).first()   
        chat.liked_by.append(user)
        db.session.add(chat)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'success': False})

#view group messages
@app.route("/api/v1/view_message/<group_id>", methods=['GET','POST'])
@login_is_required
def view_message(group_id):
    try:          
        group=Group.query.filter_by(id=int(group_id)).first()
        message_data=[]
        for chat in group.chats:
            data={
            "chat_id": chat.id,
            "message": chat.message,
            "chat_by_id": chat.chat_by[0].id,
            "chat_by_name": chat.chat_by[0].username,
            "liked_by_id": chat.liked_by,
            "timestamp": chat.time
            }
            message_data.append(data)
        print(message_data)
        final_data={
            "message_data": message_data,
            "success": True
        }
        return jsonify(final_data)
    except Exception as e:
        print(e)
        return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True)