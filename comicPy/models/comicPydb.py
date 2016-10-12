from datetime import datetime
from comicPy.models import db


class comicvine_api_history(db.Model):
    __tablename__ = 'comicvine_api_history'
    id = db.Column(db.Integer(), primary_key=True)
    request_url = db.Column('request_url', db.String)
    json_response = db.Column('json_response', db.String)
    created = db.Column('created', db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


# class issue(object):
#     def __init__(self, issue_id="",
#                  publisher_name="",
#                  volume_name="",
#                  volume_issue_number="",
#                  description="",
#                  issue_path="",
#                  issue_cover_path="",
#                  issue_filename="",
#                  synced_with_comicvine=""):
#         self.issue_id = issue_id
#         self.publisher_name = publisher_name
#         self.volume_name = volume_name
#         self.volume_issue_number = volume_issue_number
#         self.description = description
#         self.issue_path = issue_path
#         self.issue_cover_path = issue_cover_path
#         self.issue_filename = issue_filename
#         self.synced_with_comicvine = synced_with_comicvine


class issue:
    def __init__(self,
                 issue_id,
                 issue_number=None,
                 cover_path=None,
                 cover_date=None,
                 store_date=None,
                 description=None,
                 path=None,
                 filename=None,
                 publisher=None,
                 volume=None,
                 characters=None,
                 concepts=None,
                 locations=None,
                 objects=None,
                 persons=None,
                 story_arcs=None,
                 teams=None,
                 synced_with_cv=None,
                 cv_issue_info=None):
        self.issue_id = issue_id
        self.issue_number = issue_number
        self.cover_path = cover_path
        self.cover_date = cover_date
        self.store_date = store_date
        self.description = description
        self.path = path
        self.filename = filename
        self.publisher = publisher
        self.volume = volume
        self.characters = characters
        self.concepts = concepts
        self.locations = locations
        self.objects = objects
        self.persons = persons
        self.story_arcs = story_arcs
        self.teams = teams
        self.synced_with_cv = synced_with_cv
        self.cv_issue_info = cv_issue_info


class publisher:
    def __init__(self,
                 publisher_id=None,
                 name=None,
                 description=None,
                 volumes=None,
                 synced_with_cv=None,
                 cv_publisher_info=None):
        self.publisher_id = publisher_id
        self.name = name
        self.description = description
        self.volumes = volumes
        self.synced_with_cv = synced_with_cv
        self.cv_publisher_info = cv_publisher_info


class volume:
    def __init__(self,
                 volume_id=None,
                 name=None,
                 description=None,
                 start_year=None,
                 count_of_issues_have=None,
                 count_of_issues=None,
                 issues=None,
                 publisher=None,
                 characters=None,
                 concepts=None,
                 locations=None,
                 objects=None,
                 persons=None,
                 teams=None,
                 synced_with_cv=None,
                 cv_volume_info=None):
        self.volume_id = volume_id
        self.name = name
        self.description = description
        self.start_year = start_year
        self.count_of_issues_have = count_of_issues_have
        self.count_of_issues = count_of_issues
        self.issues = issues
        self.publisher = publisher
        self.characters = characters
        self.concepts = concepts
        self.locations = locations
        self.objects = objects
        self.persons = persons
        self.teams = teams
        self.synced_with_cv = synced_with_cv
        self.cv_volume_info = cv_volume_info

# class character:
#     def __init__(self,
#                  character_id,
#                  name,
#                  description,
#                  issues,
#                  publisher,
#                  creators,
#                  teams,
#                  synced_with_cv,
#                  cv_volume_info):
#
#
# class concept:
#
#
# class location:
#
#
# class object:
#
#
# class person:
#
#
# class story_arc:
#
#
# class team:
