from wtforms import Form, SelectField

class CoursesForm(Form):
    course = SelectField('Courses', choices=[('Python-Base', 'Python-Base'),('Python-Database', 'Python-Database'),
        ('HTML', 'HTML'),('Java-Base', 'Java-Base'),('JavaScript Base', 'JavaScript Base')], default=1)