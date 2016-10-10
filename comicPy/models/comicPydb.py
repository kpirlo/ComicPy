from datetime import datetime
from comicPy.models import db


class comicvine_api_history(db.Model):
    __tablename__ = 'comicvine_api_history'
    id = db.Column(db.Integer(), primary_key=True)
    request_url = db.Column('request_url', db.String)
    json_response = db.Column('json_response', db.String)
    created = db.Column('created', db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class issue(object):
    def __init__(self, issue_id="",
                 publisher_name="",
                 volume_name="",
                 volume_issue_number="",
                 description="",
                 issue_path="",
                 issue_cover_path="",
                 issue_filename="",
                 synced_with_comicvine=""):
        self.issue_id = issue_id
        self.publisher_name = publisher_name
        self.volume_name = volume_name
        self.volume_issue_number = volume_issue_number
        self.description = description
        self.issue_path = issue_path
        self.issue_cover_path = issue_cover_path
        self.issue_filename = issue_filename
        self.synced_with_comicvine = synced_with_comicvine
