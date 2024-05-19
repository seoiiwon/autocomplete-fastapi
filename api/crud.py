from api.models import Post
from sqlalchemy.orm import Session
from datetime import datetime


def get_post_list(db : Session):
    post_list = db.query(Post).order_by(Post.date.desc()).all()
    return post_list

def search_posts(db : Session, keyword : str):
    search = f"%{keyword}%"
    return db.query(Post).filter(Post.subject.like(search) | Post.content.like(search)).all()
