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
    issue_response = queryComicVineApi('issue', issue_id, '')
    if issue_response:
        issue_aliases = response['results']['aliases']
        issue_api_detail_url = response['results']['api_detail_url']
        issue_character_credits = response['results']['character_credits']
        issue_character_died_in = response['results']['character_died_in']
        issue_concept_credits = response['results']['concept_credits']
        issue_cover_date = response['results']['issue_cover_date']
        issue_date_added = response['results']['issue_date_added']
        issue_date_last_updated = response['results']['issue_date_last_updated']
        issue_deck = response['results']['issue_deck']
        issue_description = response['results']['issue_description']
        issue_first_appearance_characters = response['results']['issue_first_appearance_characters']
        issue_first_appearance_concepts = response['results']['issue_first_appearance_concepts']
        issue_first_appearance_locations = response['results']['issue_first_appearance_locations']
        issue_first_appearance_objects = response['results']['issue_first_appearance_objects']
        issue_first_appearance_storyarcs = response['results']['issue_first_appearance_storyarcs']
        issue_first_appearance_teams = response['results']['issue_first_appearance_teams']
        issue_has_staff_review = response['results']['issue_has_staff_review']
        issue_image = response['results']['issue_image']
        issue_issue_number = response['results']['issue_issue_number']
        issue_location_credits = response['results']['issue_location_credits']
        issue_name = response['results']['issue_name']
        issue_object_credits = response['results']['issue_object_credits']
        issue_person_credits = response['results']['issue_person_credits']
        issue_site_detail_url = response['results']['issue_site_detail_url']
        issue_store_date = response['results']['issue_store_date']
        issue_story_arc_credits = response['results']['issue_story_arc_credits']
        issue_team_credits = response['results']['issue_team_credits']
        issue_team_disbanded_in = response['results']['issue_team_disbanded_in']
        issue_volume = response['results']['issue_volume']

        for item in issue_character_credits.items():
            print "character credit - api_detail_url: " + item[0]
            print "character credit - id: " + item[1]
            # check if we have character ID synced first

            character_response = queryComicVineApi('character', item[1], '')
            if character_response:
                print "character response"
                character_aliases = character_response['results']['aliases']
                character_api_detail_url = character_response['results']['character_api_detail_url']
                character_birth = character_response['results']['character_birth']
                character_character_enemies = character_response['results']['character_character_enemies']
                character_character_friends = character_response['results']['character_character_friends']
                character_count_of_issue_appearances = character_response['results']['character_count_of_issue_appearances']
                character_creators = character_response['results']['character_creators']
                character_date_added = character_response['results']['character_date_added']
                character_date_last_updated = character_response['results']['character_date_last_updated']
                character_deck = character_response['results']['character_deck']
                character_description = character_response['results']['character_description']
                character_first_appeared_in_issue = character_response['results']['character_first_appeared_in_issue']
                character_gender = character_response['results']['character_gender']
                character_id = character_response['results']['character_id']
                character_image = character_response['results']['character_image']
                character_issue_credits = character_response['results']['character_issue_credits']
                character_issues_died_in = character_response['results']['character_issues_died_in']
                character_movies = character_response['results']['character_movies']
                character_name = character_response['results']['character_name']
                character_origin = character_response['results']['character_origin']
                character_powers = character_response['results']['character_powers']
                character_publisher = character_response['results']['character_publisher']
                character_real_name = character_response['results']['character_real_name']
                character_site_detail_url = character_response['results']['character_site_detail_url']
                character_story_arc_credits = character_response['results']['character_story_arc_credits']
                character_team_enemies = character_response['results']['character_team_enemies']
                character_team_friends = character_response['results']['character_team_friends']
                character_teams = character_response['results']['character_teams']
                character_volume_credits = character_response['results']['character_volume_credits']

            print "character credit - name: " + item[2]
            print "character credit - site_detail_url: " + item[3]




        # insert issue_characters
        # comicPy_conn = sqlite3.connect(comicPy_db_location)
        # with comicPy_conn:
        #     cur = comicPy_conn.cursor()
        #     for character in response['results']['character_credits'].items():
        #         cur.execute("INSERT INTO issue_characters (issue_id, character_id) VALUES (?, ?)", issue_id, character[1])

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
