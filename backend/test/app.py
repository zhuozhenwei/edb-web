import pymysql
import os
import json
from flask import Flask, request, abort, jsonify, session, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 启用 CORS

app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024  # 只接受最大为1MB的请求
app.config["UPLOAD_EXTENSIONS"] = [".txt", ".json"]  # 确保文件扩展名的正确


@app.route("/", methods=["GET", "POST"])
def select():
    # Get the data from the request payload
    data = request.get_json()

    # Access the selected option and other data
    input_value = data.get("inputValue")
    selected_option = data.get("selectedOption")

    if input_value == "":
        select_str = "SELECT * FROM poc_test"
    elif selected_option == "cve-id":
        select_str = "SELECT * FROM poc_test WHERE CVE_ID LIKE '%" + input_value + "%'"
    elif selected_option == "software":
        select_str = (
            "SELECT * FROM poc_test WHERE software_version LIKE '%" + input_value + "%'"
        )
    elif selected_option == "platform":
        select_str = (
            "SELECT * FROM poc_test WHERE test_platform LIKE '%" + input_value + "%'"
        )
    else:
        select_str = (
            "SELECT * FROM poc_test WHERE "
            + selected_option
            + " LIKE '%"
            + input_value
            + "%'"
        )

    print(select_str)
    db = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="123456",
        database="poc",
        charset="utf8mb4",
    )

    # 创建游标对象
    cursor = db.cursor()

    # 执行SELECT查询
    cursor.execute(select_str)

    # 获取查询结果的属性信息
    columns = [desc[0] for desc in cursor.description]

    # 打印属性列
    print(columns)

    # 获取查询结果
    results = cursor.fetchall()
    """
    # 打印每一行数据
    for row in results:
        print(row)
    """
    print(f"find {len(results)} result(s)")
    # 关闭游标
    cursor.close()

    db.close()

    data = []
    columns = [desc[0] for desc in cursor.description]

    for row in results:
        data.append(dict(zip(columns, row)))

    return jsonify(data)


# 添加跨域支持
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    return response


# 上传文件
@app.route("/upload", methods=["POST"])
def uploadFile():
    if "file" in request.files:
        file = request.files["file"]
        filename = file.filename

        # 创建一个新文件夹
        file_path = os.path.join("D:\\Code\\edb-web\\backend\\poc", filename)
        file_path = file_path[:-5]
        os.mkdir(file_path)  # 在路径file_path首先创建一个文件夹
        os.chmod(file_path, 0o755)
        app.config["UPLOAD_PATH"] = file_path  # 上传路径

        if filename == "":
            return {"message": "No selected file"}  # 没有选择文件
        else:
            print(f"The file's name is {filename}")
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
                abort(400)
            file.save(os.path.join(app.config["UPLOAD_PATH"], filename))

            # 用户上传的.json文件增加一个Verified字段，未经审核默认都为0
            with open(file_path + "\\" + filename, "r", encoding="utf-8") as f:
                old_data = json.load(f)
                old_data["Verified"] = "0"  # 后台管理员审核修改界面
            with open(file_path + "\\" + filename, "w", encoding="utf-8") as f:
                json.dump(old_data, f)

        return {
            "code": 200,
            "messsge": "File uploaded successfully",  # 成功上传
            "fileName": filename,
        }
    else:
        return {"message": "File is not received"}  # 前端还未传来


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
