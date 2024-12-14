# Flask网站框架
# jsonify将数据转换为 JSON 格式
# 处理json数据
import json
from flask import (Flask, request,
                   jsonify,url_for,render_template)
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

# 获取当前文件所在目录的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app) # 启用跨域支持

# 配置上传文件存储路径
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello():
     return """
        This is the home page. <br>
        <a href="ai">这里有ai回答</a><br>
        <a href="login">可以去登录页面</a><br>
        <a href="about">Go to about page</a><br>
        """


@app.route('/ask')
def ask():
    # 如果用户通过POST方法提交表单
    if request.method == 'POST':
        # 从表单中获取数据
        gender = request.form.get('gender')
        username = request.form.get('username')
        age = request.form.get('age')
        email = request.form.get('email')
        isPregnant = request.form.get('isPregnant')
        pa = request.form.get('PA')
        userLabelData = request.form.getlist('userLabelData')
        userLabelCandidates = request.form.getlist('userLabelCandidates')
        # 将获取的数据存储在一个字典中
        user_info = {
            "gender": gender,
            "username": username,
            "age": age,
            "email": email,
            "isPregnant": isPregnant,
            "PA": pa,
            "userLabelData": userLabelData,
            "userLabelCandidates": userLabelCandidates
        }

        # 将用户信息保存到一个名为'user_data.json'的文件中
        with open('user_data.json', 'w') as f:
            json.dump(user_info, f)
        # 返回一个JSON响应，告诉用户数据已成功保存
        return jsonify({"message": "Data saved successfully."})
    else:
        # 如果不是POST请求，返回一个HTML表单，让用户可以输入数据
        return """
        This is the home page. <br>
        <a href="ai">这里有ai回答</a><br>
        <a href="login">可以去登录页面</a><br>
        <a href="{}">Go to about page</a><br>
        <form method="post">
            <label for="gender">Gender:</label>
            <input type="text" id="gender" name="gender"><br>

            <label for="username">Username:</label>
            <input type="text" id="username" name="username"><br>

            <label for="age">Age:</label>
            <input type="text" id="age" name="age"><br>

            <label for="email">Email:</label>
            <input type="text" id="email" name="email"><br>

            <label for="isPregnant">Is Pregnant:</label>
            <input type="text" id="isPregnant" name="isPregnant"><br>

            <label for="PA">Physical Activity (PA):</label>
            <input type="text" id="PA" name="PA"><br>

            <label for="userLabelData">User Label Data (multiple selection):</label><br>
            <input type="checkbox" name="userLabelData" value="高血压患者">高血压患者<br>
            <input type="checkbox" name="userLabelData" value="注重精神健康">注重精神健康<br>

            <label for="userLabelCandidates">User Label Candidates (multiple selection):</label><br>
            <input type="checkbox" name="userLabelCandidates" value="中年人">中年人<br>
            <input type="checkbox" name="userLabelCandidates" value="糖尿病患者">糖尿病患者<br>
            <input type="checkbox" name="userLabelCandidates" value="高血压患者">高血压患者<br>
            <input type="checkbox" name="userLabelCandidates" value="注重精神健康">注重精神健康<br>

            <input type="submit" value="Submit"><br>
        </form>
        
    <form action="upload" method="post" enctype="multipart/form-data">
    <input type="file" name="image" accept="image/*">
    <input type="submit" value="Upload Image">
    </form>
        """.format(url_for('about'))


@app.route('/about')
def about():
    return 'This is the about page.'

@app.route('/login')
def login():
    username = 'John'
    return render_template('login.html', name=username)

import new_chat
@app.route('/ai')
def ai():
    food_name="苹果"
    user_desc="18岁不健康男性"
    # 示例用户信息字典
    user_info = {
        "gender": "男",
        "username": "张三峰",
        "age": "18",
        "email": "trial-email@163.com",
        "isPregnant": "否",
        "PA": "中",
        "userLabelData": [
            "高血压患者",
            "注重精神健康",
        ],
        "userLabelCandidates": [
            "中年人",
            "糖尿病患者",
            "高血压患者",
            "注重精神健康",
        ]
    }
    output=new_chat.handle_food_info_get(food_name, user_desc, user_info)
    return output

@app.route('/upload_image', methods=['POST'])
def upload_image():
    print("收到上传请求")  # 添加日志
    if 'image' not in request.files:
        print("没有文件")  # 添加日志
        return jsonify({
            'success': False,
            'message': 'No file part'
        })
    file = request.files['image']
    if file.filename == '':
        return jsonify({
            'success': False,
            'message': 'No selected file'
        })
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({
            'success': True,
            'data': {
                'filename': filename
            }
        })
    return jsonify({
        'success': False,
        'message': 'File type not allowed'
    })

@app.route('/get_result_detail', methods=['POST'])
def get_result_detail():
    try:
        # 这里调用 new_chat.py 中的函数处理识别结果
        food_name = "苹果" # 这里应该是从图像识别结果获取
        user_desc = "18岁健康男性"
        
        # 从请求中获取用户信息
        user_info = request.get_json()
        if not user_info:
            user_info = {
                "gender": "男",
                "username": "测试用户",
                "age": "18",
                "email": "test@example.com",
                "isPregnant": "否",
                "PA": "中",
                "userLabelData": ["注重健康"],
                "userLabelCandidates": [
                    "年轻人",
                    "注重健康"
                ]
            }
            
        result = new_chat.handle_food_info_get(food_name, user_desc, user_info)
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

if __name__ == '__main__':
    app.run()


    
