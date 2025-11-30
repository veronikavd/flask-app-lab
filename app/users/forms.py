from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(min=4, max=10, message="Довжина імені має бути від 4 до 10 символів")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Email(message="Некоректний email")
    ])
    phone = StringField('Phone', validators=[
        DataRequired(),
        Regexp(r'^\+380\d{9}$', message="Формат: +380XXXXXXXXX")
    ])
    subject = SelectField('Subject', choices=[
        ('general', 'Загальне питання'),
        ('bug', 'Повідомити про помилку'),
        ('collab', 'Співпраця')
    ])
    message = TextAreaField('Message', validators=[
        DataRequired(),
        Length(max=500, message="Максимум 500 символів")
    ])
    submit = SubmitField('Send')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Введіть ім'я користувача")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Введіть пароль"),
        Length(min=4, max=10, message="Пароль має бути від 4 до 10 символів")
    ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')