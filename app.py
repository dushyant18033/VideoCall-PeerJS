from flask import Flask, render_template, request, session
import os

app = Flask(__name__)

userType = {'student': 0, 'teacher': 1}


class user:
    def __init__(self, uname, passwd, utype):
        self.uname = uname
        self.passwd = passwd
        self.utype = utype

    def __str__(self):
        return self.uname + "," + self.passwd + "," + self.utype

    def checkPwd(self, passwd):
        return self.passwd == passwd


def exists(uname):
    for i in set_users:
        if uname == i.uname:
            return i
    return None


set_users = set()

set_users.add(user('dush', 'panch', 'teacher'))
set_users.add(user('dush1', 'panch', 'student'))


@app.route('/', methods=['POST', 'GET'])
def login():  # login screen interaction
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
                session['logged_in'] = True
                return render_template('JoinASession.html', user=us)
            else:
                return render_template('home.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():  # sign up page interaction
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
                set_users.add(user(uname, passwd, utype))
                return render_template('home.html')
            else:
                return render_template('signup.html')


@app.route('/begin', methods=['POST', 'GET'])
def begin():
    if session.get('logged_in'):
        cur_user = exists(request.form.get('username'))
        return render_template('master.html', user=cur_user)
    else:
        return login()


@app.route('/join', methods=['POST', 'GET'])
def join():
    if session.get('logged_in'):
        cur_user = exists(request.form.get('username'))
        ssid = request.form.get('TpeerID')
        return render_template('slave.html', user=cur_user, TpeerID=ssid)
    else:
        return login()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    print('py called')
    return login()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', debug=True, ssl_context=('cert.pem', 'key.pem'))
    #app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
