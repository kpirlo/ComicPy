"""
Routes and views for the flask application.
"""

# from datetime import datetime
from flask import render_template, g, redirect, url_for
from comicPy import app
from models.mylar import mylar_comics, mylar_issues
from models.security import User, Role
from models.comicPydb import *
from flask_security import current_user, Security, SQLAlchemyUserDatastore, login_required, roles_required
from config import *
from functions import getIssueImage, synced_with_comicPy, sync_with_comicvine, resize_image
import zipfile
import rarfile
import sqlite3
import os
import os.path

import pprint

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.before_request
def load_user():
    if current_user.is_authenticated:
        g.user_id = current_user.get_id()  # return username in get_id()
    else:
        g.user_id = None  # or 'some fake value', whatever


@app.route('/')
@app.route('/home')
@login_required
def home():
    # get newest cover_date and select all with that cover_date
    # profile info
    # new releases
    # user reading list
    # user reading history

    comicPy_conn = sqlite3.connect(comicPy_db_location)
    with comicPy_conn:
        cur = comicPy_conn.cursor()
        cur.execute("SELECT issue_id, description, image, folder_path, filename, synced_with_comicvine "
            "FROM issues WHERE cover_date = (SELECT cover_date FROM issues ORDER BY cover_date DESC LIMIT 1) LIMIT 3")
        new_releases = cur.fetchall()
        new_releases_list = []
        for row in new_releases:
            # create new list to hold new release issue objects
            # create new object for issue
            issue_instance = issue()
            issue_instance.issue_id = row[0]
            issue_instance.issue_path = root_comics_folder + row[3] + "/" + row[4]
            issue_instance.issue_filename = row[4]
            if not os.path.isfile(issue_instance.issue_path):
                print "File Missing.."
                issue_instance.issue_cover_image_path = "static\\media\\missing_file.jpg"
            else:
                # try to get comicvine info if we have not

                # if unable to get comic vine or no cover exists at least make a cover:
                if not os.path.isfile("comicPy\\static\\media\\issue_covers\\" + row[0] + ".jpg"):
                    if not os.path.isfile("comicPy\\static\\media\\issue_covers\\" + row[0] + "-page1.jpg"):
                        # issue_cover_image_path = extract_cover()
                        # extract first page and save as image
                        print "extracting first page"
                        if row[4][-4:] == '.cbr':
                            print 'cbr'
                            with rarfile.RarFile(issue_path, "r") as r:
                                pages = r.namelist()
                                pages.sort()
                                r.extract(pages[0], "comicPy\\static\\media\\issue_covers\\")
                                os.rename("comicPy\\static\\media\\issue_covers\\" + pages[0],
                                          "comicPy\\static\\media\\issue_covers\\" + row[0] + "-page1.jpg")
                                resize_image("comicPy\\static\\media\\issue_covers\\" + row[0] + "-page1.jpg")

                        elif row[4][-4:] == '.cbz':
                            print 'cbz'
                            with zipfile.ZipFile(issue_path, "r") as z:
                                pages.sort()
                                z.extract(pages[0], "comicPy\\static\\media\\issue_covers\\")
                                os.rename("comicPy\\static\\media\\issue_covers\\" + pages[0],
                                          "comicPy\\static\\media\\issue_covers\\" + row[0] + "-page1.jpg")
                                resize_image("comicPy\\static\\media\\issue_covers\\" + row[0] + "-page1.jpg")
                        else:
                            print 'fuck if i know'
                    issue_instance.issue_cover_image_path = "static\\media\\issue_covers\\" + row[0] + "-page1.jpg"
            new_releases_list.append(issue_instance)

            for obj in new_releases_list:
                print "inside new list of issue objects"
                print obj.issue_id

                        # if row[3] is None or row[3] is False:
                        #     print "not synced with comicvine"
                        #     print "trying sync"
                        #     if sync_with_comicvine(row[0]):
                        #         print "synced"
                        #     else:
                        #         print "not synced"
                        # else:
                        #     print "synced already? "

    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        newReleases=new_releases_list,
        user=current_user,
        year=datetime.now().year,
    )


    # TODO make a way to browse folder items not in mylar.

    #     { % if current_user.has_role('admin') %}
    #      < li > < a href = "#" > Manage Site < / a > < / li >
    #     { % endif %}

    # new_releases = mylar_issues.query.filter_by(Status="Downloaded").order_by(mylar_issues.IssueDate.desc(),
    #                                                                           mylar_issues.ReleaseDate.desc()).limit(5)\
    #                                                                           .all()

    # for issue in new_releases:
    #     # check if we have synced this issue with comicPy db.
    #     if not synced_with_comicPy(issue.IssueID):
    #         print "Not in comicPy db"
    #     else:
    #         print "in comicPy! "
    #         # insert_issue_into_comicPy(issue)
    #
    #     issue.IssueImageURL = getIssueImage(issue.IssueID)

    # print g.user_id


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


@app.route('/syncMylar')
@roles_required('admin')
def syncMylar():
    print "sync"
    mylar_conn = sqlite3.connect(MylarDbLocation)
    with mylar_conn:
        cur = mylar_conn.cursor()
        cur.execute("SELECT issues.IssueID AS issue_id, issues.ComicID AS volume_id, IssueDate AS cover_date, "
                    "replace(comics.ComicLocation,'/media/dataroot/media/comics/','') AS issue_folder_path, "
                    "issues.Location AS issue_filename"
                    " FROM issues"
                    " LEFT JOIN comics ON issues.ComicID = comics.ComicID "
                    "WHERE issues.Status = 'Downloaded'")
        issues_mylar = cur.fetchall()

    comicPy_conn = sqlite3.connect(comicPy_db_location)
    with comicPy_conn:
        cur2 = comicPy_conn.cursor()
        cur2.execute("SELECT issue_id FROM issues")
        issues_comicPy = [row[0] for row in cur2.fetchall()]

    no_match = [issue for issue in issues_mylar if issue[0] not in issues_comicPy]

    for item in no_match:
        comicPy_conn = sqlite3.connect(comicPy_db_location)
        with comicPy_conn:
            cur = comicPy_conn.cursor()
            cur.execute("INSERT INTO issues (issue_id, volume_id, cover_date, folder_path, filename) "
                        "VALUES (?,?,?,?,?)", (item[0], item[1], item[2], item[3], item[4]))

    # Remove ones not in mylar any more from database.

    return redirect(url_for('home'))


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
