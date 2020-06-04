from flask import Flask, render_template, jsonify, request
import json
import utils
import ast

app = Flask(__name__)


constraints = {
    "required": "BẮT BUỘC nhập liệu",
    "email": "Dữ liệu nhập đúng định dạng EMAIL",
    "url": "Dữ liệu nhập là địa chỉ URL",
    "max_len": "Chiều dài TỐI ĐA dữ liệu nhập",
    "min_len": "Chiều dài TỐI THIỂU dữ liệu nhập",
    "is_range": "Nhập số trong KHOẢNG GIÁ TRỊ chỉ định",
    "is_digit": "Dữ liệu nhập là các KÝ SỐ",
    "is_lowercase": "Dữ liệu nhập là các KÝ TỰ THƯỜNG",
    "is_uppercase": "Dữ liệu nhập là các KÝ TỰ HOA",
    "is_punctuation": "Dữ liệu nhập các ký tự DẤU CÂU hoặc KÝ TỰ ĐẶC BIỆT",
    "required_selected": "BẮT BUỘC CHỌN trong danh sách",
    "required_checked": "BẮT BUỘC CHECK chọn",
    "pattern": "Dữ liệu nhập phải KHỚP với một biểu thức chính quy"
}

data_types = {
    "string": "Kiểu chuỗi",
    "number": "Kiểu số",
    "boolean": "Kiểu luận lý"
}

controls = {
    "max_len": [{
        "type": "number",
        "display": "Nhập chiều dài tối đa cho phép",
        "conditions": ["<= %s", "> %s"]
    }],
    "min_len": [{
        "type": "number",
        "display": "Nhập chiều dài tối thiểu cho phép",
        "conditions": [">= %s", "< %s"]
    }],
    "range": [{
        "type": "number",
        "display": "Số bắt đầu",
        "conditions": [">= %s", "< %s"]
    }, {
        "type": "number",
        "display": "Số kết thúc",
        "conditions": ["<= %s", "> %s"]
    }],
    "pattern": [{
        "type": "text",
        "display": "Nhập mẫu biểu thức chính quy"
    }]
}


@app.route("/")
def index():
    return render_template("index.html",
                           constraints=constraints,
                           controls=json.dumps(controls),
                           data_types=data_types)


@app.route("/controls/<cons>", methods=["GET"])
def get_controls(cons):
    if controls.get(cons):
        return jsonify({"controls": controls[cons]})

    return jsonify({"controls": {}})


import threading


class MyThread(threading.Thread):
    def __init__(self, clf, names, class_names):
        threading.Thread.__init__(self)
        self.clf = clf
        self.names = names
        self.class_names = class_names

    def run(self):
        utils.draw_decision_tree(self.clf, self.names, self.class_names)


@app.route("/tcs", methods=["POST"])
def generate_tcs():
    X = ast.literal_eval(request.form["X"])
    y = ast.literal_eval(request.form["y"])
    for idx_y, r in enumerate(X):
        while -1 in r:
            idx = r.index(-1)
            r[idx] = 1
            r1 = r.copy()
            r1[idx] = 0
            if r1 not in X:
                X.append(r1)
                y.append(y[idx_y])

    names = ast.literal_eval(request.form["names"])
    constraints = ast.literal_eval(request.form["constraints"])

    tcs = utils.generate_testcase(X=X, y=y, constraints=constraints, names=names)
    # clf = utils.build_tree(X=X, y=y)
    # utils.draw_decision_tree(clf=clf, names=names, class_names=list(set(y)))

    # MyThread(clf, names, list(set(y))).start()

    return jsonify({"success": True, "data": tcs})


if __name__ == "__main__":
    app.run()
