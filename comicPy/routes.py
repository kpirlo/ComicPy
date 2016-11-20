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
    # get values if comicvine api exists and comicvine is enabled.


@app.route('/')
@app.route('/home')
@login_required
def home():
    # get newest cover_date and select all with that cover_date
    # profile info
    #
    missing_files_list = []
    # new releases
    # create new list to hold new release issue objects
    new_releases_list = []
    # user reading list
    # user reading history

    comicPy_conn = sqlite3.connect(comicPy_db_location)
    with comicPy_conn:
        cur = comicPy_conn.cursor()
        cur.execute("SELECT "
                    "issues.issue_id, "
                    "issues.description, "
                    "issues.issue_number, "
                    "issues.path, "
                    "issues.filename, "
                    "issues.synced_with_cv, "
                    "volumes.name AS volume_name, "
                    "volumes.start_year AS volume_start_year, "
                    "volumes.publisher AS volume_publisher "
                    "FROM issues "
                    "LEFT JOIN volumes on issues.volume_id = volumes.volume_id "
                    "WHERE cover_date = (SELECT cover_date FROM issues ORDER BY cover_date DESC LIMIT 1) LIMIT 2")
        new_releases = cur.fetchall()

        for row in new_releases:
            # create new object for each issue
            issue_instance = issue(issue_id=row[0])
            issue_instance.path = root_comics_folder + row[3] + "/" + row[4]
            issue_instance.filename = row[4]
            issue_instance.synced_with_cv = row[5]
            # try to query comicvine
            # if comicvine enabled
            # if comicvine api key exists
            #   sync_with_comicvine(issue_instance.issue_id)
            # else error no key
            # move into function to get issue_cover_image_path()
            # is cv enabled/key set?
            if CV_API_KEY and not CV_API_KEY == "":
                if not issue_instance.synced_with_cv or issue_instance.synced_with_cv == "":
                    print "issue not synced"
                    print "attempting sync"
                    # sync_with_cv(issue, issue_instance.issue_id)
                else:
                    print "already synced on DATE"
            else:
                print "CV KEY MISSING - Will not attempt any sync"

            # check file system for cover
            if not os.path.isfile("comicPy\\static\\media\\issue_covers\\" + issue_instance.issue_id + ".jpg"):
                # if no cover , check file system for page1 as cover.
                if not os.path.isfile("comicPy\\static\\media\\issue_covers\\" + issue_instance.issue_id + "-page1.jpg"):
                    # No page1 exists, extract page1 for cover.
                    # extract_issue_page(issue_instance.issue_id, "1")
                    #   --paramaters issue_id, page_number or ALL -- try to extract into memory
                    # if returned
                    # save returned object in cover directory
                    # else fail could not extract (add to failed_issues_list ?)

                    if os.path.isfile(issue_instance.path):
                        print "extracting first page" + issue_instance.path
                        if issue_instance.filename[-4:] == '.cbr':
                            print 'cbr'
                            with rarfile.RarFile(issue_instance.path, "r") as r:
                                pages = r.namelist()
                                pages.sort()
                                r.extract(pages[0], "comicPy\\static\\media\\issue_covers\\")
                                os.rename("comicPy\\static\\media\\issue_covers\\" + pages[0],
                                          "comicPy\\static\\media\\issue_covers\\" + issue_instance.issue_id + "-page1.jpg")
                                resize_image("comicPy\\static\\media\\issue_covers\\" + issue_instance.issue_id + "-page1.jpg")

                        elif issue_instance.filename[-4:] == '.cbz':
                            print 'cbz'
                            with zipfile.ZipFile(issue_instance.path, "r") as z:
                                pages = z.namelist()
                                pages.sort()
                                z.extract(pages[0], "comicPy\\static\\media\\issue_covers\\")
                                os.rename("comicPy\\static\\media\\issue_covers\\" + pages[0],
                                          "comicPy\\static\\media\\issue_covers\\" + issue_instance.issue_id + "-page1.jpg")
                                resize_image("comicPy\\static\\media\\issue_covers\\" + issue_instance.issue_id + "-page1.jpg")
                        else:
                            print 'fuck if i know'

                issue_instance.cover_path = "static\\media\\issue_covers\\" + issue_instance.issue_id + "-page1.jpg"

            if os.path.isfile(issue_instance.path):
                new_releases_list.append(issue_instance)
            else:
                missing_files_list.append(issue_instance)

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
                    "issues.Location AS issue_filename, Issue_Number AS issue_number"
                    " FROM issues"
                    " LEFT JOIN comics ON issues.ComicID = comics.ComicID "
                    "WHERE issues.Status = 'Downloaded'")
        issues_mylar = cur.fetchall()

    mylar_conn = sqlite3.connect(MylarDbLocation)
    with mylar_conn:
        cur = mylar_conn.cursor()
        cur.execute("SELECT DISTINCT issues.ComicID AS volume_id, comics.ComicName AS comic_name, "
                    "comics.ComicYear AS start_year, comics.ComicPublisher AS volume_publisher_name,  "
                    "replace(comics.ComicLocation,'/media/dataroot/media/comics/','') AS issue_folder_path "
                    " FROM issues"
                    " LEFT JOIN comics ON issues.ComicID = comics.ComicID "
                    "WHERE issues.Status = 'Downloaded'")
        volumes_mylar = cur.fetchall()

    mylar_conn = sqlite3.connect(MylarDbLocation)
    with mylar_conn:
        cur = mylar_conn.cursor()
        cur.execute("SELECT DISTINCT ComicPublisher AS volume_publisher_name "
                    " FROM issues"
                    " LEFT JOIN comics ON issues.ComicID = comics.ComicID "
                    "WHERE issues.Status = 'Downloaded'")
        publishers_mylar = [row[0] for row in cur.fetchall()]

    comicPy_conn = sqlite3.connect(comicPy_db_location)
    with comicPy_conn:
        cur = comicPy_conn.cursor()
        cur.execute("SELECT issue_id FROM issues")
        issues_comicPy = [row[0] for row in cur.fetchall()]

    comicPy_conn = sqlite3.connect(comicPy_db_location)
    with comicPy_conn:
        cur = comicPy_conn.cursor()
        cur.execute("SELECT volume_id FROM volumes")
        volumes_comicPy = [row[0] for row in cur.fetchall()]

    comicPy_conn = sqlite3.connect(comicPy_db_location)
    with comicPy_conn:
        cur = comicPy_conn.cursor()
        cur.execute("SELECT name FROM publishers")
        publishers_comicPy = [row[0] for row in cur.fetchall()]

    no_match_issues = [issue for issue in issues_mylar if issue[0] not in issues_comicPy]
    no_match_volumes = [volume for volume in volumes_mylar if volume[0] not in volumes_comicPy]
    no_match_publishers = set(publishers_mylar) - set(publishers_comicPy)

    for item in no_match_issues:
        comicPy_conn = sqlite3.connect(comicPy_db_location)
        with comicPy_conn:
            cur = comicPy_conn.cursor()
            cur.execute("INSERT INTO issues (issue_id, volume_id, cover_date, folder_path, filename, volume_issue_number) "
                        "VALUES (?,?,?,?,?,?)", (item[0], item[1], item[2], item[3], item[4], item[5]))

    for item in no_match_volumes:
        print "add volume"
        comicPy_conn = sqlite3.connect(comicPy_db_location)
        with comicPy_conn:
            cur = comicPy_conn.cursor()
            cur.execute("INSERT INTO volumes (volume_id, name, start_year, publisher, volume_folder_path) "
                        "VALUES (?,?,?,?,?)", (item[0], item[1], item[2], item[3], item[4]))

    for item in no_match_publishers:
        print "add publisher"
        comicPy_conn = sqlite3.connect(comicPy_db_location)
        with comicPy_conn:
            cur = comicPy_conn.cursor()
            cur.execute("INSERT INTO publishers (name) "
                        "VALUES (?)", (item,))

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


@app.route('/extract/<issue_id>/<page_number>')
@login_required
def extract(issue_id=None, page_number="all"):


    """Renders the home page."""
    return render_template(
        'browseVolumeId.html',
        title='Browse Publisher',
        volumeIssues=volumeIssues,
        year=datetime.now().year,
    )
