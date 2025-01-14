# Flask网站框架
# jsonify将数据转换为 JSON 格式
# 处理json数据
import json
from flask import (
    Flask, request,jsonify,url_for,render_template
)
from blueprints import (
    ai,auth,posts,image
)
from flask_migrate import Migrate
from exts import db,mail
import config
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

# 获取当前文件所在目录的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

# 绑定配置文件
app.config.from_object(config)

# 配置数据库和邮箱
db.init_app(app)
mail.init_app(app)
migrate=Migrate(app,db)


# 注册蓝图
app.register_blueprint(ai.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(posts.posts_bp, url_prefix='/api/v1/posts')
app.register_blueprint(image.bp)
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
        <a href="ai/response">这里有ai回答</a><br>
        <a href="about">Go to about page</a><br>
        """




@app.route('/about')
def about():
    return 'This is the about page.'


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


    
