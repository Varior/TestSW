
from flaskext.mysql import MySQL

class MysqlCommands(MySQL):
    """docstring for MysqlCommands"""
    def __init__(self):
        super(MysqlCommands, self).__init__()

    def count_all(self):
        self.cursor = self.connect().cursor()
        self.cursor.callproc('count_all')
        self.total = self.cursor.fetchone()
        self.cursor.close()
        return self.total

    def find(self, name):
        self.name = name
        self.cursor = self.connect().cursor()
        self.cursor.callproc('find_user',(self.name,))
        self.users = self.cursor.fetchall()
        self.cursor.close()
        return self.users
    
    def pagination(self, start, records):
        self.start = start
        self.records = records
        self.cursor = self.connect().cursor()
        self.cursor.callproc('pagination', (self.start, self.records))
        self.users = self.cursor.fetchall()
        self.cursor.close()
        return self.users

    def create_user(self, name, email, phone, mphone, status):
        self.name = name
        self.email = email
        self.phone = phone
        self.mphone = mphone
        self.status = status
        self.cursor = self.connect().cursor()
        self. cursor.callproc('create_user',(self.name, self.email,self.phone, self.mphone, self.status))
        self.cursor.close()
        return "User created successfully"

    def delete_user(self, user_id):
        self.user_id = user_id
        self.cursor = self.connect().cursor()
        self. cursor.callproc('delete_user',(self.user_id,))
        self.cursor.close()

    def find_user(self, user_id):
        self.user_id = user_id
        self.cursor = self.connect().cursor()
        self. cursor.callproc('select_user',(self.user_id,))
        self.user = self.cursor.fetchone()
        self.cursor.close()
        return self.user

    def find_user_courses(self, user_id):
        self.user_id = user_id
        self.cursor = self.connect().cursor()
        self. cursor.callproc('find_course',(self.user_id,))
        self.courses = self.cursor.fetchall()
        self.cursor.close()
        return self.courses

    def change_user_info(self, user_id, user_email, phone, mphone, user_status):
        self.user_id = user_id
        self.user_email = user_email
        self.phone = phone
        self.mphone = mphone
        self.user_status = user_status
        self.cursor = self.connect().cursor()
        self. cursor.callproc('update_user',(self.user_id, self.user_email, self.phone, self.mphone, self.user_status))
        self.cursor.close()
        return "Changes saved successfully"

    def create_course(self, user_id, course_name, course_code):
        self.user_id = user_id
        self.course_name = course_name
        self.course_code = course_code
        self.cursor = self.connect().cursor()
        self. cursor.callproc('create_course',(self.course_name, self.course_code, self.user_id))
        self.cursor.close()

    def delete_course(self, user_id, course_code):
        self.user_id = user_id
        self.course = course_code
        self.cursor = self.connect().cursor()
        self. cursor.callproc('delete_course',(user_id, course_code))
        self.cursor.close()