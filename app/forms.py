from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DateField, SelectField, SubmitField, BooleanField, SelectMultipleField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import TextArea
from datetime import datetime
from flask_login import current_user
from .models import User, Tag, CATEGORIES 
from . import db 

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Паролі повинні збігатися')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = db.session.execute(db.select(User).filter_by(email=email.data)).scalar_one_or_none()
        if user:
            raise ValidationError('Ця електронна пошта вже використовується.')

    def validate_username(self, username):
        user = db.session.execute(db.select(User).filter_by(username=username.data)).scalar_one_or_none()
        if user:
            raise ValidationError('Це ім\'я користувача вже зайняте.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    about_me = StringField('About Me', widget=TextArea(), validators=[Length(max=140)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = db.session.execute(db.select(User).filter_by(username=username.data)).scalar_one_or_none()
            if user:
                raise ValidationError('Це ім\'я користувача вже зайняте.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = db.session.execute(db.select(User).filter_by(email=email.data)).scalar_one_or_none()
            if user:
                raise ValidationError('Ця електронна пошта вже використовується.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2)])
    content = StringField('Content', widget=TextArea(), validators=[DataRequired(), Length(min=5, max=500)])
    is_active = BooleanField('Is this post active?', default=True)
    publish_date = DateField('Publish Date', format='%Y-%m-%d', default=datetime.utcnow)
    category = SelectField('Category', choices=CATEGORIES, validators=[DataRequired()])
    tags = SelectMultipleField('Tags', coerce=int)
    submit = SubmitField('Add Post')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tags_list = db.session.execute(db.select(Tag).order_by(Tag.name)).scalars().all()
        self.tags.choices = [(t.id, t.name) for t in tags_list]