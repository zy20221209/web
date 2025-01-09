# forms.py

import wtforms
from wtforms.validators import Email,Length,EqualTo
from models import UserModel,EmailCaptchaModel
from exts import db
# Form：主要就是用来验证前端提交的数据是否符合要求
class RegisterForm(wtforms.Form):
    email=wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password=wtforms.StringField(validators=[Length(min=6,max=20,message="密码格式错误")])
    password_confirm=wtforms.StringField(validators=[EqualTo("password")])
    captcha=wtforms.StringField(validators=[Length(min=6,max=6,message="验证码格式错误！")])


    def validate(self):
        email=self.email.data
        user=UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册！")
        
    def validate_captcha(self):
        captcha=self.captcha.data
        email=self.email.data
        captcha_model= EmailCaptchaModel.query.filter_by(email=email,captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或验证码错误！")
        else:
            db.session.delete(captcha)
            db.session.commit()

class LoginForm(wtforms.Form):
    email=wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password=wtforms.StringField(validators=[Length(min=6,max=20,message="密码格式错误")])
