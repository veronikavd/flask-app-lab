from . import db
from typing import List
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, Boolean, Text, ForeignKey, Enum, Table, Column
from flask_login import UserMixin

CATEGORIES = [
    ('Tech', 'Technology'), 
    ('Art', 'Art'), 
    ('Science', 'Science'), 
    ('Lifestyle', 'Lifestyle')
]

post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    
    posts: Mapped[List["Post"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    publish_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    category: Mapped[str] = mapped_column(Enum(*[c[0] for c in CATEGORIES], name='post_categories'), default='Tech')

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    
    tags: Mapped[List["Tag"]] = relationship(
        secondary=post_tags,
        back_populates="posts"
    )
    
    def __repr__(self):
        return f'<Post {self.title}>'

class Tag(db.Model):
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(80), unique=True, nullable=False)

    posts: Mapped[List["Post"]] = relationship(
        secondary=post_tags,
        back_populates="tags"
    )
    
    def __repr__(self):
        return f'<Tag {self.name}>'