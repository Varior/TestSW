import os.path
from flask import Flask, request, redirect, render_template, send_from_directory
from flaskext.mysql import MySQL
from form.userForms import UserForm

mysql = MySQL()
app = Flask(__name__, static_url_path='')


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1111'
app.config['MYSQL_DATABASE_DB'] = 'Users'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route('/user', methods=['GET'])
@app.route('/', methods=['GET'])
def users_list():
    qs = request.args.get("sname", type=str)
    rec = request.args.get("records", 10,type=int)
    if qs:
        cursor = mysql.connect().cursor()
        cursor.callproc('find_user',(qs,))
        users = cursor.fetchall()
        cursor.close()
        return render_template('users.html', users=users)
    cursor = mysql.connect().cursor()
    cursor.callproc('find_all')
    users = cursor.fetchall()
    cursor.close()
    return render_template('users.html', users=users)


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
    msg=''
    cursor = mysql.connect().cursor()
    cursor.callproc('select_user',(user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:  
        form = UserForm(request.form)
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
            msg='successful update'
            return redirect("/")    
        return render_template('user_add.html', form=form)
        #return render_template('user_info.html', user=user, profile=profile, form=form, msg=msg)
    return render_template('error.html', msg_eror="not id {}".format(user_id))


'''@app.route('/user/<owner_id>/delete/course', methods=['GET'])
def course_delete(owner_id):
    user_id = request.args.get("user_id")
    owner_id=int(owner_id)  
    if user_id:
        user_id=int(user_id)
        del_contact = Contacts.query.filter_by(owner_id=owner_id, user_id=user_id).first()
        db.session.delete(del_contact)
        db.session.commit()
        _url = '/user/' + str(owner_id)+ '/contact'
        return redirect(_url)
    return render_template('error.html', msg_eror="not id {}".format(user_id))'''





@app.route('/del')
def del_user(): pass


if __name__ == '__main__':
    app.run(debug=True)