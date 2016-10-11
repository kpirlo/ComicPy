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


class issue_info:
    def __init__(self,
                 issue_id,
                 issue_number,
                 cover_date,
                 store_date,
                 description,
                 path,
                 cover_path,
                 filename,
                 publisher,
                 volume,
                 synced_with_cv,
                 cv_issue_info):
        self.issue_id = issue_id
        self.issue_number = issue_number
        self.cover_date = cover_date
        self.store_date = store_date
        self.description = description
        self.path = path
        self.cover_path = cover_path
        self.filename = filename
        self.publisher = publisher
        self.volume = volume
        self.synced_with_cv = synced_with_cv
        self.cv_issue_info = cv_issue_info


class publisher:
    def __init__(self,
                 publisher_id,
                 name,
                 description,
                 path,
                 image_path,
                 image_filename,
                 synced_with_cv,
                 cv_publisher_info):
        self.publisher_id = publisher_id
        self.name = name
        self.description = description
        self.path = path
        self.image_path = image_path
        self.image_filename = image_filename
        self.synced_with_cv = synced_with_cv
        self.cv_publisher_info = cv_publisher_info


class volume:
    def __init__(self,
                 volume_id,
                 name,
                 description,
                 start_year,
                 synced_with_cv,
                 cv_volume_info):
        self.volume_id = volume_id
        self.name = name
        self.description = description
        self.start_year = start_year
        self.synced_with_cv = synced_with_cv
        self.cv_volume_info = cv_volume_info

class character:


class concept:


class location:


class object:


class person:


class story_arc:


class team:
