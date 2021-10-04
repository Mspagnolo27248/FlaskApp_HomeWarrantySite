#Flask_Auth/project_files/models.py
from project_files import db,app,login_manager #imports from __init.py
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)#this is a sql alchemy query that returna user model from an id input


#Class models, UserMixin allows us to check if a user is logged in. 

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    address = db.Column(db.String(128),unique=True,index=True)
    tickets = db.relationship('TicketModel',backref='tickets',lazy='dynamic')

    def __init__(self,email,username,password,address):
         self.email = email
         self.username = username
         self.password_hash = generate_password_hash(password)
         self.address = address

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


class TicketModel(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer,primary_key=True)
    home_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    #owner = db.Column(db.Text) #swap for id
    desc = db.Column(db.Text)
    create_date = db.Column(db.Text) #MMDDYYYY
    close_date = db.Column(db.Text)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))

    def __init__(self,home_id,desc,create_date,close_date='99999999',category_id=None):
        #self.home_id = home_id
        self.home_id = home_id
        self.desc = desc
        self.create_date = create_date
        self.close_date = close_date
        self.category_id = category_id
    def __repr__(self):
        return f"{self.home_id},{self.desc},{self.category_id},{self.create_date},{self.close_date}"

class CategoryModel(db.Model):
    __tablename__='category'

    id = db.Column(db.Integer,primary_key=True)
    category = db.Column(db.Text)
    

    def __init__(self,category):
        self.category = category
        super().__init__()
    
    def __repr__(self):
        return f"{self.category}"

