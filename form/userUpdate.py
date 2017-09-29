from wtforms import Form, StringField, SelectField, validators
from wtforms.validators import Required, Email, Optional

class UserUpdate(Form):
    name = StringField('Name')
    email = StringField('E-mail', validators = [Required(),Email()])
    phone = StringField('Phone')
    m_phone = StringField('Mobile phone')
    status = SelectField('Status', coerce=int, choices=[(1, 'Active'),(0, 'Inactive')], default=0)