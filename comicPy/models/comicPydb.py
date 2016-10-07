from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from comicPy.models import db

class cache_comics(db.Model):
    __tablename__ = 'cache_comics'
    id = db.Column(db.Integer(), primary_key=True)
    comicID =  db.Column ('comicID', db.String )
    cv_volume_id =  db.Column ('cv_volume_id', db.String )
    created =  db.Column ('created', db.String )

class cache_issues(db.Model):
    __tablename__ = 'cache_issues'
    id = db.Column(db.Integer(), primary_key=True)
    issueID =  db.Column ('issueID', db.String )
    issue_image_url =  db.Column ('issue_image_url', db.String )
    created =  db.Column ('created', db.String )

    def __init__ (self):
        self.id = id
        self.issueID = issueID
        self.issue_image_url = issue_image_url
        self.created = created

    
class comicvine_api_history(db.Model):
    __tablename__ = 'comicvine_api_history'
    id = db.Column(db.Integer(), primary_key=True)
    request_url = db.Column('request_url', db.String)
    json_response = db.Column('json_response', db.String)
    created = db.Column('created', db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
