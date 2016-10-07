# from datetime import datetime
# from comicPy.models import db
# from models.mylar import mylar_comics, mylar_issues
from models.comicPydb import *
from config import *
import urllib
import json
# import re
# from pprint import pprint
import sqlite3


def sync_with_comicvine(issue_id):
    response = queryComicVineApi('issue', issue_id, '')
    if response:
        print "queried comic vine issue"
        for i in response['results']['image'].items():
            print i[0]
            print i[1]

        # parse, query other objects as needed
        # then store in database
    return True


def synced_with_comicPy(issue_id):
    # look up issue_id in comicPy database return yes/no
    mylarConn = sqlite3.connect(comicPy_db_location)
    with mylarConn:
        cur = mylarConn.cursor()
        cur.execute("SELECT issue_id FROM issues WHERE issue_id = ?", (issue_id,))
        if cur.fetchone():
            synced = 1
        else:
            synced = 0
    return synced


def queryComicVineApi(type, id, querystr):
    if type == 'comic':
        typeid = '4050'
    elif type == 'issue':
        typeid = '4000'
    elif type == 'publisher':
        typeid = '4010'

    queryURL = 'http://comicvine.gamespot.com/api/' + type + '/' + typeid + '-' + id + '/?api_key=' + CV_API_KEY + querystr + '&format=json'
    response = urllib.urlopen(queryURL)
    ComicVineApiResponseJSONStr = response.read()
    ComicVineApiResponseJSON = json.loads(ComicVineApiResponseJSONStr)

    # record all api calls in db
    print "adding api response to local database"
    new_record = comicvine_api_history(request_url=queryURL, json_response=ComicVineApiResponseJSONStr)
    db.session.add(new_record)
    db.session.commit()

    return ComicVineApiResponseJSON


def getIssueImage(issueID):
    # check database
    # use api
    # use blank default if none

    cache_issue = None
    # cache_issues.query.filter_by(issueID=issueID).order_by(cache_issues.created.desc()).first()

    if cache_issue is None:
        print 'cache_issue empty'
        issue_image_url = queryComicVineApi('issue', issueID, '&field_list=image')['results']['image']['thumb_url']
    elif cache_issue.issue_image_url is None or cache_issue.issue_image_url == '':
        print 'no local image found in cache_issue'
        issue_image_url = queryComicVineApi('issue', issueID, '&field_list=image')['results']['image']['thumb_url']
    else:
        issue_image_url = cache_issue.issue_image_url
        print issue_image_url
    return str(issue_image_url)
