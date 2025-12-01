from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms import DateTimeLocalField
from datetime import datetime

CATEGORIES = [
    ('news', 'Новини'),
    ('publication', 'Публікація'),
    ('tech', 'Технології'),
    ('other', 'Інше')
]

class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[
        DataRequired(message="Введіть заголовок"),
        Length(min=5, max=150)
    ])
    content = TextAreaField('Зміст', render_kw={"rows": 5}, validators=[
        DataRequired(message="Текст посту обов'язковий")
    ])
    is_active = BooleanField('Активний пост', default=True)
    publish_date = DateTimeLocalField('Дата публікації', format="%Y-%m-%dT%H:%M", default=datetime.now)
    category = SelectField('Категорія', choices=CATEGORIES, validators=[DataRequired()])
    submit = SubmitField('Зберегти пост')