# auth.py
from .forms import RegisterForm,LoginForm
from flask import (
    Blueprint,request,jsonify,render_template,redirect,url_for
)
from models import UserModel,EmailCaptchaModel
from exts import db,mail
from flask_mail import Message
import string
import random
from werkzeug.security import generate_password_hash,check_password_hash

# 蓝图auth
bp=Blueprint("auth",__name__,url_prefix="/auth")

@bp.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    email=form.email.data
    password=form.password.data
    user=UserModel.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': '账号不存在'}), 401
    if check_password_hash(user.password,password):
        return jsonify({'message': '登录成功'}), 200
    else:
        return jsonify({'message': '密码错误'}), 401


# 注册账号
@bp.route("/register",methods=['POST'])
def register():
    form = RegisterForm(request.form)
    if not form.validate_captcha():
        return jsonify({'message': '验证码错误：{{form.errors}}'}), 401
    if form.validate():
        email=form.email.data
        password=form.password.data
        user=UserModel(email=email,password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': '注册成功'}), 200
    else:
        print(form.errors)
        return jsonify({'message': '格式错误：{{form.errors}}'}), 400

# 获取邮箱验证码
@bp.route("/captcha/email",methods=['POST'])
def get_email_captcha():
    
    # 邮箱账号
    email=request.args.get("email")
    # 随机六个数字
    source=string.digits*6
    captcha=random.sample(source,6)
    captcha="".join(captcha)
    # 由洛夜的qq账号向用户发送验证码
    message=Message(subject="网站注册验证码",recipients=["3278934211@qq.com"],body=f"您的验证码是：{captcha}")
    mail.send(message)
    # 将验证码保存到数据库
    email_captcha=EmailCaptchaModel(email=email,captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({"code":200,"message":"验证码获取成功","data":None})
