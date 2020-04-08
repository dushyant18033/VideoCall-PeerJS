from flask import Flask, render_template, request

app = Flask(__name__)

userType = {'student': 0, 'teacher': 1}


class user:
    # peerID = username
    def __init__(self, uname, passwd, utype):
        self.uname = uname
        self.passwd = passwd
        self.utype = utype

    def __str__(self):
        return self.uname + "," + self.passwd + "," + self.utype

    def checkPwd(self, passwd):
        return self.passwd == passwd


class session:
    def __init__(self, sid, teacher):
        self.sess_id = sid
        self.teacher = teacher
        self.students = set()

    def student_join(self, stud):
        self.students.add(stud)

    def __str__(self):
        string = str(self.sess_id)
        for i in self.students:
            string += str(i)
        return string


def exists(uname):
    for i in list_users:
        if uname == i.uname:
            return i
    return None


list_users = set()
list_sessions = dict()

list_users.add(user('dush', 'panch', 'teacher'))
list_users.add(user('dush1', 'panch', 'student'))


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
                list_users.add(user(uname, passwd, utype))
                return render_template('home.html')
            else:
                return render_template('signup.html')


@app.route('/begin', methods=['POST', 'GET'])
def begin():  # session join/create interaction
    cur_user = exists(request.form.get('username'))
    sess = session('0000'+str(len(list_sessions)), cur_user)
    list_sessions[sess.sess_id] = sess
    return render_template('master.html', session=sess, user=cur_user)


@app.route('/join', methods=['POST', 'GET'])
def join():
    cur_user = exists(request.form.get('username'))
    ssid = request.form.get('sessionid')
    if ssid in list_sessions:
        sess = list_sessions[ssid]
        sess.student_join(cur_user)
        return render_template('slave.html', session=sess, user=cur_user)
    else:
        return render_template('home.html')


'''
@app.route('/join', methods=['POST','GET'])
def joinASession():
    if request.method == 'GET':
        return render_template('JoinASession.html')
    else:
        sid = request.form.get('sessionid')
'''

if __name__ == "__main__":
    app.run(debug=True)
