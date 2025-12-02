from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea
from datetime import datetime

from .models import User, Tag, CATEGORIES 
from . import db 

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2)])
    content = StringField('Content', widget=TextArea(), validators=[DataRequired(), Length(min=5, max=500)])
    is_active = BooleanField('Is this post active?', default=True)
    publish_date = DateField('Publish Date', format='%Y-%m-%d', default=datetime.utcnow)
    category = SelectField('Category', choices=CATEGORIES, validators=[DataRequired()])
    
    author_id = SelectField('Author', coerce=int, validators=[DataRequired()])
    tags = SelectMultipleField('Tags', coerce=int)
    
    submit = SubmitField('Add Post')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        authors = db.session.execute(db.select(User).order_by(User.id)).scalars().all()
        self.author_id.choices = [(author.id, author.username) for author in authors]
        
        tags_list = db.session.execute(db.select(Tag).order_by(Tag.name)).scalars().all()
        self.tags.choices = [(t.id, t.name) for t in tags_list]