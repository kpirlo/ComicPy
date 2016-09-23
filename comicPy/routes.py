"""
Routes and views for the flask application.
"""

# from datetime import datetime
from flask import render_template
from comicPy import app
from models.mylar import mylar_comics, mylar_issues
from models.security import User, Role
from models.comicPydb import *
from flask_security import Security, SQLAlchemyUserDatastore, login_required, roles_required
from config import *
from functions import getIssueImage
import zipfile
import rarfile
import sqlite3

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route('/')
@app.route('/home')
@login_required
def home():
    # get latest 5 comics to display on home page
    new_releases = mylar_issues.query.filter_by(Status="Downloaded").order_by(mylar_issues.ReleaseDate.desc()).limit(
        5).all()
    for issue in new_releases:
        issue.IssueImageURL = getIssueImage(issue.IssueID)

    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        newReleases=new_releases,
        year=datetime.now().year,
    )


@app.route('/browse')
@app.route('/browse/publishers/')
@login_required
def browse():
    # group by publisher, comic, issue, tags?
    # sort by name, release, added
    # future save settings per user
    # browse/publisher/<publisher>
    # browse/volume/<volume>
    # browse/

    mylarConn = sqlite3.connect(MylarDbLocation)
    with mylarConn:
        cur = mylarConn.cursor()
        cur.execute("SELECT DISTINCT ComicPublisher FROM comics")
        publishers = [row[0] for row in cur.fetchall()]
        for publisher in publishers:
            print publisher

    """Renders the home page."""
    return render_template(
        'browse.html',
        title='Browse Comics',
        publishers=publishers,
        year=datetime.now().year,
    )


@app.route('/browse/publisher/<publisherId>')
@login_required
def browsePublisherId(publisherId=None):
    mylarConn = sqlite3.connect(MylarDbLocation)
    with mylarConn:
        cur = mylarConn.cursor()
        cur.execute("SELECT DISTINCT ComicName FROM comics WHERE ComicPublisher = ?", (publisherId,))
        comicVolumes = [row[0] for row in cur.fetchall()]
        for comicVolume in comicVolumes:
            print comicVolume

    """Renders the home page."""
    return render_template(
        'browsePublisher.html',
        title='Browse Publisher',
        comicVolumes=comicVolumes,
        year=datetime.now().year,
    )


@app.route('/browse/volume/<volumeId>')
@login_required
def browseVolumeId(volumeId=None):
    mylarConn = sqlite3.connect(MylarDbLocation)
    with mylarConn:
        cur = mylarConn.cursor()
        cur.execute("SELECT DISTINCT ComicName, Issue_Number, IssueID FROM issues WHERE ComicID = ?", (volumeId,))
        volumeIssues = cur.fetchall()
        for volumeIssue in volumeIssues:
            print volumeIssue

    """Renders the home page."""
    return render_template(
        'browseVolumeId.html',
        title='Browse Publisher',
        volumeIssues=volumeIssues,
        year=datetime.now().year,
    )


@app.route('/settings')
@roles_required('admin')
def settings():
    return render_template(
        'settings.html',
        title='settings',
        year=datetime.now().year,
    )


@app.route('/comic/issue/<issueID>')
def issueDetail(issueID):
    """Renders the Issue Details page."""
    IssueList = mylar_issues.query.filter_by(IssueID=issueID).order_by(mylar_issues.ReleaseDate.desc()).first()
    ComicInfo = mylar_comics.query.filter_by(ComicID=IssueList.ComicID).first()
    IssuePath = ComicInfo.ComicLocation + '/' + IssueList.Location
    print IssuePath
    IssuePath = 'C:\\blue.cbr'

    if IssueList.Location[-4:] == '.cbr':
        print 'cbr'
        with rarfile.RarFile(IssuePath, "r") as r:
            pages = r.namelist()
            for page in pages:
                print page
        r.extractall("comicPy\\static\\temp")

    elif IssueList.Location[-4:] == '.cbz':
        print 'cbz'
        with zipfile.ZipFile(IssuePath, "r") as z:
            pages = z.namelist()
            for page in pages:
                print page

        z.extractall("comicPy\\static\\temp")
    else:
        print 'fuck if i know'

    return render_template(
        'issueDetail.html',
        title='Issue Detail',
        year=datetime.now().year,
        Issue=IssueList,
        pages=pages,
        message='List Issue Details'
    )
