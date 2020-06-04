from prompt_toolkit.layout import is_dimension
from sklearn import tree
from pprint import pprint
import random
import string
import uuid
import sys

# headers = ["username_required", "username_lowercase",
#            "password_required", "password_lowercase",
#            "password_len_gte_10"]
# X = [
#     [0, -1, -1, -1, -1],
#     [-1, 0, -1, -1, -1],
#     [-1, -1, 0, -1, -1],
#     [-1, -1, -1, 0, -1],
#     [-1, -1, -1, -1, 0],
#     [1, 1, 1, 1, 1]
# ]
# y = [1, 2, 3, 2, 2, 9]
headers = ['u_required', 'u_number', 'p_required', 'p_number', 'p_punctuation', 'p_uppercase', 'p_lowercase']
X = [[0, -1, -1, -1, -1, -1, -1], [-1, 0, -1, -1, -1, -1, -1], [-1, -1, 0, -1, -1, -1, -1], [-1, -1, -1, 0, -1, -1, -1], [-1, -1, -1, -1, 0, -1, -1], [-1, -1, -1, -1, -1, 0, -1], [-1, -1, -1, -1, -1, -1, 0], [1, 1, 1, 1, 1, 1, 1]]
y = ['blank', 'invalid', 'blank', 'invalid', 'invalid', 'invalid', 'invalid', 'valid']


def generate_str(len_str=6, **kwargs):
    """
    Hàm sinh ra một chuỗi ngẫu nhiên theo yều cầu
    :param len_str: chiều dài chuỗi
    :param is_lowercase: chứa ký tự thường
    :param is_uppercase: chứa ký tự hoa
    :param is_digit: chứa ký số
    :param is_punctuation: chứa dấu câu hoặc ký tự đặc biệt
    :return: Chuỗi được sinh ra
    """
    characters = ""
    kq = ""
    if kwargs.get("is_lowercase"):
        characters += string.ascii_lowercase
        kq += random.choice(string.ascii_lowercase)
    if kwargs.get("is_uppercase"):
        characters += string.ascii_uppercase
        kq += random.choice(string.ascii_uppercase)
    if kwargs.get("is_digit"):
        characters += string.digits
        kq += random.choice(string.digits)
    if kwargs.get("is_punctuation"):
        characters += string.punctuation
        kq += random.choice(string.punctuation)

    if len(kq) > len_str:
        raise Exception("Cannot generate the string!")

    kq = [kq] + [random.choice(characters) for _ in range(len_str-len(kq))]
    random.shuffle(kq)

    return "".join(kq)


def generate_uuid():
    return uuid.uuid4()


def get_boundary_values(min_num=None, max_num=None, decimal_places=0):
    """
    Hàm sinh ra giá trị biên của một khoảng chỉ định
    :param min_num: số bắt đầu
    :param max_num: số kết thúc
    :param decimal_places: số chữ số thậ phân xác định biên
    :return: danh sách các giá trị được chọn
    """
    if min_num and max_num and max_num < min_num:
        raise Exception("Invalid input!")

    step = pow(10, -decimal_places)

    k = []
    if min_num:
        # biên dưới
        k.append(min_num)
        # cận biên dưới
        k.append(min_num + step)

    if max_num:
        # biên trên
        k.append(max_num)
        # cận biên trên
        k.append(max_num - step)

    # k.append(round(random.uniform(min_num if min_num else -sys.maxsize, max_num if max_num else sys.maxsize), decimal_places))

    return k


def generate_email(is_valid=True):
    """
    Tạo ra một địa chỉ email
    :param is_valid: True để nhận email hợp lệ, ngược lại sinh email không hợp lệ
    :return: email
    """
    extensions = ['com', 'net', 'org', 'gov']
    domains = ['gmail', 'yahoo', 'comcast', 'verizon', 'charter', 'hotmail', 'outlook', 'frontier']

    winext = extensions[random.randint(0, len(extensions) - 1)]
    windom = domains[random.randint(0, len(domains) - 1)]

    acclen = random.randint(1, 20)

    winacc = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(acclen))

    finale = winacc + "@" + ((windom + "." + winext) if is_valid else "")
    return finale


def generate_url():
    pass


def build_tree(X, y):
    clf = tree.DecisionTreeClassifier()
    clf.fit(X, y)

    return clf


def generate_data(constraints={}):
    """

    :param constraints: {
        "username___string": {
            "required": "",
            "is_lowercase": "",
            "is_uppercase": "",
            "is_digit": "",
            "is_punctuation": ""
        }
    }
    :return:
    """
    data = {}

    for k, v in constraints.items():
        d = k.split("___")
        data[k] = []

        if d[1] == "string":

            # Sinh theo ký tự
            params = {}
            if "min_len" in v:
                params["min_num"] = int(v["min_len"].strip(","))
            if "max_len" in v:
                params["max_num"] = int(v["max_len"].strip(","))

            if len(params) > 0:
                str_len = [int(k) for k in get_boundary_values(**params)]
            else:
                str_len = [6]

            data[k].append(["", "required___0"])

            for length in str_len:
                is_lowercase = "is_lowercase" in v
                is_uppercase = "is_uppercase" in v
                is_digit = "is_digit" in v
                is_punctuation = "is_punctuation" in v
                if is_lowercase:
                    data[k].append([generate_str(is_lowercase=True, len_str=length),
                                    "required___1", "is_lowercase___1"])
                    data[k].append([generate_str(is_uppercase=True, is_digit=True, is_punctuation=True, len_str=length),
                                   "required___1", "is_lowercase___0", "is_uppercase___1",
                                    "is_digit___1", "is_punctuation___1"])
                if is_uppercase:
                    data[k].append([generate_str(is_uppercase=True, len_str=length),
                                    "required___1", "is_uppercase___1"])
                    data[k].append([generate_str(is_lowercase=True, is_digit=True, is_punctuation=True, len_str=length),
                                   "required___1", "is_lowercase___1",
                                    "is_uppercase___0", "is_digit___1", "is_punctuation___1"])
                if is_digit:
                    data[k].append([generate_str(is_digit=True, len_str=length),
                                    "required___1", "is_digit___1"])
                    data[k].append([generate_str(is_lowercase=True, is_uppercase=True, is_punctuation=True, len_str=length),
                                   "required___1", "is_lowercase___1", "is_uppercase___1",
                                    "is_digit___0", "is_punctuation___1"])
                if is_punctuation:
                    data[k].append([generate_str(is_punctuation=True, len_str=length),
                                    "required___1", "is_punctuation___1"])
                    data[k].append([generate_str(is_lowercase=True, is_uppercase=True, is_digit=True, len_str=length),
                                   "required___1", "is_lowercase___1", "is_uppercase___1",
                                    "is_digit___1", "is_punctuation___0"])

                if is_lowercase and is_uppercase:
                    data[k].append([generate_str(is_lowercase=True, is_uppercase=True, len_str=length),
                                    "required___1", "is_lowercase___1", "is_uppercase___1"])

                if is_lowercase and is_digit:
                    data[k].append([generate_str(is_lowercase=True, is_digit=True, len_str=length),
                                    "required___1", "is_lowercase___1", "is_digit___1"])

                if is_lowercase and is_punctuation:
                    data[k].append([generate_str(is_lowercase=True, is_punctuation=True, len_str=length),
                                    "required___1", "is_lowercase___1", "is_punctuation___1"])

                if is_uppercase and is_digit:
                    data[k].append([generate_str(is_uppercase=True, is_digit=True, len_str=length),
                                    "required___1", "is_uppercase___1", "is_digit___1"])

                if is_uppercase and is_punctuation:
                    data[k].append([generate_str(is_uppercase=True, is_punctuation=True, len_str=length),
                                   "required___1", "is_uppercase___1", "is_punctuation___1"])

                if is_digit and is_punctuation:
                    data[k].append([generate_str(is_digit=True, is_punctuation=True, len_str=length),
                                    "required___1", "is_digit___1", "is_punctuation___1"])

                if is_lowercase and is_uppercase and is_digit and is_punctuation:
                    data[k].append([generate_str(is_lowercase=True, is_uppercase=True,
                                                 is_digit=True, is_punctuation=True, len_str=length),
                                   "required___1", "is_lowercase___1", "is_uppercase___1",
                                    "is_digit___1", "is_punctuation___1"])

            # Sinh theo email
            if "email" in v:
                data[k].append([generate_email(), "required___1", "email___1"])
                data[k].append([generate_email(is_valid=False), "required___1", "email___0"])
        elif d[1] == "number":
            pass
        elif d[1] == "boolean":
            pass

    return data


def generate_testcase(X, y, constraints, names):
    """
    Sinh test case tự động
    :param X: [
        [0, -1, -1, -1],
        [-1, 0, -1, -1],
        [-1, -1, 0, -1],
        [-1, -1, -1, 0],
        [1, 1, 1, 1]
    ]
    :param y: [-1, -1, -1, -1, 1]
    :param constraints: {
        "username___string": {
            "required": "true",
            "email": "true"
        },
        "password___string": {
            "required": "true",
            "is_lowercase": "true"
        }
    }
    :param names: ["username___required", "username___email", "password___required", "password___is_lowercase"]
    :return:
    """
    clf = build_tree(X, y)
    data = generate_data(constraints=constraints)

    keys = list(data.keys())

    tcs = []
    for d in data[keys[0]]:
        vector = [0] * len(names)
        # inp = [d[0]]
        # Cập nhật vector
        for i in range(1, len(d)):
            k = d[i].split("___")

            t = "%s___%s" % (keys[0].split("___")[0], k[0])
            print(t)
            if t in names:
                idx = names.index(t)
                vector[idx] = int(k[1])

        for d1 in data[keys[1]]:
            # inp.append(d1[0])
            # Cập nhật vector
            for i in range(1, len(d1)):
                k = d1[i].split("___")
                t = "%s___%s" % (keys[1].split("___")[0], k[0])
                print(t)
                if t in names:
                    idx = names.index(t)
                    vector[idx] = int(k[1])

            # inp.append(clf.predict([vector]))
            print("======")
            print("[%s %s %s]" % (d[0] if d[0] != "" else "_",
                                  d1[0] if d1[0] != "" else "_",
                                  str(vector)))
            t = vector.copy()
            tcs.append([d[0], d1[0], str(clf.predict([vector])[0]), t])
    pprint(tcs)
    return tcs


def draw_decision_tree(clf, names, class_names, img_name="imagename.png"):
    import matplotlib.pyplot as plt
    tree.plot_tree(clf)
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(4, 4), dpi=300)

    tree.plot_tree(clf,
                   feature_names=names,
                   class_names=class_names,
                   filled=True)

    fig.savefig(img_name)


if __name__ == "__main__":
    pass
    # import matplotlib.pyplot as plt
    # clf = build_tree(X, y)
    # print(clf.predict([[1, 1, 1, 1, 1]]))
    # tree.plot_tree(clf)
    # fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(4, 4), dpi=300)
    # tree.plot_tree(clf,
    #                feature_names=headers,
    #                class_names=["valid", "invalid", "blank"],
    #                filled=True);
    # fig.savefig('imagename.png')

    X = [[0, -1, -1], [1, 1, 1]]
    XX = []
    for r in X:
        while -1 in r:
            idx = r.index(-1)
            r1 = r.copy()
            r[idx] = 0
            r1[idx] = 1
            X.append(r1)
    pprint(X)

    # headers = ["username___required", "username___email", "password___required", "password___is_lowercase"]
    # X = [
    #     [0, -1, -1, -1],
    #     [-1, 0, -1, -1],
    #     [-1, -1, 0, -1],
    #     [-1, -1, -1, 0],
    #     [1, 1, 1, 1]
    # ]
    # y = [-1, -1, -1, -1, 1]
    #
    # generate_testcase(X, y, constraints={
    #     "username___string": {
    #         "required": "true",
    #         "email": "true"
    #     },
    #     "password___string": {
    #         "required": "true",
    #         "is_lowercase": "true"
    #     }
    #
    # }, names=headers)
    #
    # from pprint import pprint
    # pprint(tcs)
    # print(generate_str(4, is_lowercase=True, is_uppercase=True))
    # print(generate_str(10, is_lowercase=True, is_uppercase=True, is_digit=True))
    # print(generate_str(8, is_lowercase=True, is_uppercase=True, is_punctuation=True, is_digit=True))
    # print(generate_uuid())
    # print(get_boundary_values(1, 10, 2))
