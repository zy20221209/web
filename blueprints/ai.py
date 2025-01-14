from flask import (
    Blueprint,request,json,jsonify,url_for
)


import new_chat

bp=Blueprint("ai",__name__,url_prefix="/ai")

@bp.route('/response',methods=['POST'])
def ai():
    # food_name="苹果"
    # user_desc="18岁不健康男性"

    food_name = request.form.get('food_name')
    user_desc = request.form.get('user_desc')

    # # 示例用户信息字典
    # user_info = {
    #     "gender": "男",
    #     "username": "张三峰",
    #     "age": "18",
    #     "email": "trial-email@163.com",
    #     "isPregnant": "否",
    #     "PA": "中",
    #     "userLabelData": [
    #         "高血压患者",
    #         "注重精神健康",
    #     ],
    #     "userLabelCandidates": [
    #         "中年人",
    #         "糖尿病患者",
    #         "高血压患者",
    #         "注重精神健康",
    #     ]
    # }
    output=new_chat.handle_food_info_get(food_name, user_desc)
    # output=new_chat.handle_food_info_get(food_name, user_desc，user_info)
    return output


@bp.route('/ask')
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
