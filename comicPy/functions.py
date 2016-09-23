from datetime import datetime
from comicPy.models import db
from models.mylar import mylar_comics, mylar_issues
from models.comicPydb import *
from config import *
import urllib, json, re
from pprint import pprint


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
    new_record = cache_comicvine(resource_type=type, resource_id=id, request_url=queryURL,
                                 json_response=ComicVineApiResponseJSONStr)
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
