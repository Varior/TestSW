from wtforms import Form, StringField, SelectField, validators
from wtforms.validators import Required, Email, Regexp

class UserForm(Form):
    name = StringField('Name', validators = [Required(), Regexp('^[a-z]{1}[a-z\s]+')])
    email = StringField('E-mail', validators = [Required(),Email()])
    phone = StringField('Phone', validators = [Regexp('^\+[0-9]{5,15}')])
    m_phone = StringField('Mobile phone', validators = [Regexp('^\+[0-9]{5,15}')])
    status = SelectField('Status', coerce=int, choices=[(1, 'Active'),(0, 'Inactive')], default=0)