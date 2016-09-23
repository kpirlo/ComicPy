from flask_sqlalchemy import SQLAlchemy
from comicPy.models import db


class mylar_comics(db.Model):
    __bind_key__ = 'mylar'
    __tablename__ = 'Comics'
    ComicID = db.Column ('ComicID',db.Integer, primary_key=True)
    ComicName = db.Column ('ComicName', db.String ) 
    ComicYear = db.Column ('ComicYear', db.String )
    DateAdded = db.Column ('DateAdded', db.String )
    Have = db.Column ('Have', db.Integer )
    Total = db.Column ('Total', db.Integer )
    ComicImage = db.Column ('ComicImage', db.String )
    ComicPublisher = db.Column ('ComicPublisher', db.String )
    ComicLocation = db.Column ('ComicLocation', db.String )
    ComicPublished = db.Column ('ComicPublished', db.String )
    LatestIssue = db.Column ('LatestIssue', db.String )
    LatestDate = db.Column ('LatestDate', db.String )
    ComicVersion = db.Column ('ComicVersion', db.String )
    DetailURL = db.Column ('DetailURL', db.String )

class mylar_issues(db.Model):
     __bind_key__ = 'mylar'
     __tablename__ = 'issues'
     IssueID = db.Column ('IssueID',db.Integer, primary_key=True)
     IssueName = db.Column ('IssueName', db.String ) 
     IssueNumber = db.Column ('Issue_Number', db.Integer ) 
     ComicName = db.Column ('ComicName', db.String )
     DateAdded = db.Column ('DateAdded', db.String )
     Status = db.Column ('Status', db.String )
     ComicID = db.Column ('ComicID',db.Integer )
     ReleaseDate = db.Column ('ReleaseDate', db.String )
     Location = db.Column ('Location', db.String )
     IssueDate = db.Column ('IssueDate', db.String )
     

    #def getIssueImage(self, issue_id):
    #  cache_issue = cache_issues.query.filter_by(issueID=issue_id).order_by(cache_issues.created.desc()).first()
    #  if cache_issue is None: 
    #    print 'cache_issue empty' 
    #    issue_image_url = queryComicVineApi('issue', issue_id , '&field_list=image')['results']['image']['thumb_url']
    #  elif cache_issue.issue_image_url is None or cache_issue.issue_image_url == '':
    #    print 'no local image found in cache_issue' 
    #    issue_image_url = queryComicVineApi('issue', issue_id , '&field_list=image')['results']['image']['thumb_url']
    #  else:
    #    issue_image_url = cache_issue.issue_image_url
    #    print issue_image_url
    #  return str(issue_image_url)
