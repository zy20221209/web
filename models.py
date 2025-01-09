from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash
class UserModel(db.Model):
    __tablename__="user"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email=db.Column(db.String(100),nullable=False,unique=True)
    password=db.Column(db.String(256),nullable=False)
    join_time=db.Column(db.DateTime,default=datetime.now)

    def set_password(self, password):
        self.password = generate_password_hash(password)   

class EmailCaptchaModel(db.Model):
    __tablename__="email_captcha"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email=db.Column(db.String(100),nullable=False)
    captcha=db.Column(db.String(100),nullable=False)
    # used=db.Column(db.Boolean,default=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow)

    def __repr__(self):
        return f'<Post {self.title}>'