from flask import Flask, render_template, request

app = Flask(__name__)

userType = {'student': 0, 'teacher': 1}


class user:
    def __init__(self, uname, passwd, utype):
        self.uname = uname
        self.passwd = passwd
        self.utype = userType[utype]

    def __str__(self):
        return self.uname + "," + self.passwd + "," + userType

    def checkPwd(self, passwd):
        return self.passwd == passwd


def exists(uname):
    for i in list_users:
        if uname == i.uname:
            return i
    return None


list_users = list()


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        uname = request.form.get('username')
        passwd = request.form.get('password')
        if uname == '' or passwd == '':
            return render_template('home.html')
        else:
            us = exists(uname)
            if us is None:
                return render_template('home.html')
            elif us.checkPwd(passwd):
                return render_template('JoinASession.html')
            else:
                return render_template('home.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        uname = request.form.get('username')
        passwd = request.form.get('password')
        if uname == '' or passwd == '':
            return render_template('signup.html')
        else:
            utype = request.form.get('usertype')
            if utype is None:
                return render_template('signup.html')
            us = exists(uname)
            if us is None:
                list_users.append(user(uname, passwd, utype))
                return render_template('home.html')
            else:
                return render_template('signup.html')


@app.route('/join', methods=['POST','GET'])
def joinASession():
    if request.method == 'GET':
        return render_template('JoinASession.html')
    else:
        sid = request.form.get('sessionid')


if __name__ == "__main__":
    app.run(debug=True)
