import os.path
from flask import Flask, request, redirect, render_template, send_from_directory
from flask_paginate import Pagination, get_page_parameter
from flaskext.mysql import MySQL
from form.userForms import UserForm
from form.userUpdate import UserUpdate

mysql = MySQL()
app = Flask(__name__, static_url_path='')


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1111'
app.config['MYSQL_DATABASE_DB'] = 'Users'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

COURSES_DIC = {"P012345":"Python-Base","P23456":"Python-Database","H345678":"HTML",
               "J456789":"Java-Base", "JS543210":"JavaScript-Base"}

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)
        

@app.route('/', methods=['GET'])
@app.route('/user', methods=['GET'])
def users_list():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    qs = request.args.get("sname", type=str)
    rec = request.args.get("records",type=int)
    if not rec:
        rec = 10
    cursor = mysql.connect().cursor()
    cursor.callproc('count_all')
    total = cursor.fetchall()
    cursor.close()    
    if qs:
        cursor = mysql.connect().cursor()
        cursor.callproc('find_user',(qs,))
        users = cursor.fetchall()
        cursor.close()
        return render_template('users.html', users=users)
    start = page*rec-rec
    cursor = mysql.connect().cursor()
    cursor.callproc('pagination', (start, rec))
    users = cursor.fetchall()
    cursor.close()
    pagination = Pagination(page=page, total=total[0][0], per_page=rec, record_name='users')
    return render_template('users.html', users=users, pagination=pagination)


@app.route('/courses', methods=['GET'])
def courses():
    return render_template('courses.html', courses=COURSES_DIC)



@app.route('/user/add', methods=['GET','POST'])
def user_add():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        _name = form.name.data
        _email = form.email.data
        _phone = form.phone.data
        _mphone = form.m_phone.data
        _status = form.status.data
        cursor = mysql.connect().cursor()
        cursor.callproc('create_user',(_name,_email,_phone,_mphone,_status))
        cursor.close()
        return redirect('/')
    return render_template('user_add.html', form=form)


@app.route('/user/<user_id>/delete', methods=['GET'])
def user_delete(user_id):
    if user_id:
        cursor = mysql.connect().cursor()
        cursor.callproc('delete_user',(user_id,))
        cursor.close()
        return redirect('/')
    return render_template('error.html', msg_eror="not id {}".format(user_id))


@app.route('/user/<user_id>', methods=['GET','POST'])
def user_update(user_id):
    courses_fr={}
    msg=''
    cursor = mysql.connect().cursor()
    cursor.callproc('select_user',(user_id,))
    user = cursor.fetchone()
    cursor.callproc('find_course',(user_id,))
    courses = cursor.fetchall()
    cursor.close()
    if courses:
        code_col ={}
        for code in courses:
            code_col[code[2]]=code[1]
        for course in COURSES_DIC:
            if not course in code_col:
                if not course in courses_fr:
                 courses_fr[course]=COURSES_DIC[course]
    else:
        courses_fr=COURSES_DIC.copy()
    if user:  
        form = UserUpdate(request.form)
        if request.method == 'GET':
            form.name.data = user[1]
            form.email.data = user[2]
            form.phone.data = user[3]
            form.m_phone.data = user[4]
            form.status.data = user[5]
        if request.method == 'POST' and form.validate():
            _email = form.email.data
            _phone = form.phone.data
            _mphone = form.m_phone.data
            _status = form.status.data
            cursor = mysql.connect().cursor()
            cursor.callproc('update_user',(user_id,_email,_phone,_mphone,_status))
            cursor.close()            
            msg='User created successful'
            return redirect("/")    
        return render_template('user_up.html', form=form, courses=courses, courses_fr=courses_fr, user_id=user_id)       
    return render_template('error.html', msg_eror="not id {}".format(user_id))


@app.route('/user/<user_id>/<course_code>/add')
def add_course(user_id, course_code):
    course_name = COURSES_DIC[course_code]
    cursor = mysql.connect().cursor()
    cursor.callproc('create_course',(course_name,course_code,user_id,))
    cursor.close()
    return redirect("/user/{}".format(user_id)) 


@app.route('/user/<user_id>/<course_code>/delete')
def del_course(user_id, course_code):

    cursor = mysql.connect().cursor()    
    cursor.callproc('delete_course',(user_id,course_code))
    cursor.close()
    return redirect("/user/{}".format(user_id)) 


if __name__ == '__main__':
    app.run(debug=True)