
import Food_Rec
from flask import (
    Blueprint,request,jsonify
)
from PIL import Image
import io


from flask import Blueprint, request, jsonify
import Food_Rec

# 创建蓝图
bp = Blueprint("image", __name__, url_prefix="/image")

@bp.route("/res", methods=['POST'])
def login():
    # 检查是否有文件部分
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['image']
    
    # 如果用户没有选择文件，浏览器也会提交一个空的part没有filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # 确保文件是允许的类型（可选）
    if file and allowed_file(file.filename):
        try:
            # 将 FileStorage 对象转换为 PIL 图像
            img = Image.open(io.BytesIO(file.read()))
            
            # 调用 food_recognition 函数进行图像识别
            result = Food_Rec.food_recognition(img)
            
            return jsonify({
                'result': result
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file format'}), 400

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
