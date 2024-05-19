from api.models import Post
from datetime import datetime
from config.database import SessionLocal
import csv

db = SessionLocal()

def create(subject, content):
    p = Post(subject=subject, content=content, date=datetime.now())
    db.add(p)
    db.commit()

with open('brandss.csv', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    for row in csvreader:
        create(row[1], row[2])