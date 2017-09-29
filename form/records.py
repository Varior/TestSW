from wtforms import Form, SelectField

class Records(Form):
    records = SelectField(coerce=int, choices=[(10, 10),(15, 15),(20, 20)], default=10)