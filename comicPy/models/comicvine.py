class issue_cv:
    def __init__(self,
                 cv_aliases,
                 cv_api_detail_url,
                 cv_character_credits,
                 cv_character_died_in,
                 cv_concept_credits,
                 cv_cover_date,
                 cv_date_added,
                 cv_date_last_updated,
                 cv_deck,
                 cv_description,
                 cv_first_appearance_characters,
                 cv_first_appearance_concepts,
                 cv_first_appearance_locations,
                 cv_first_appearance_objects,
                 cv_first_appearance_storyarcs,
                 cv_first_appearance_teams,
                 cv_has_staff_review,
                 cv_id,
                 cv_image,
                 cv_issue_number,
                 cv_location_credits,
                 cv_name,
                 cv_object_credits,
                 cv_person_credits,
                 cv_site_detail_url,
                 cv_store_date,
                 cv_story_arc_credits,
                 cv_team_credits,
                 cv_team_disbanded_in,
                 cv_volume):
        self.cv_aliases = cv_aliases
        self.cv_api_detail_url = cv_api_detail_url
        self.cv_character_credits = cv_character_credits
        self.cv_character_died_in = cv_character_died_in
        self.cv_concept_credits = cv_concept_credits
        self.cv_cover_date = cv_cover_date
        self.cv_date_added = cv_date_added
        self.cv_date_last_updated = cv_date_last_updated
        self.cv_deck = cv_deck
        self.cv_description = cv_description
        self.cv_first_appearance_characters = cv_first_appearance_characters
        self.cv_first_appearance_concepts = cv_first_appearance_concepts
        self.cv_first_appearance_locations = cv_first_appearance_locations
        self.cv_first_appearance_objects = cv_first_appearance_objects
        self.cv_first_appearance_storyarcs = cv_first_appearance_storyarcs
        self.cv_first_appearance_teams = cv_first_appearance_teams
        self.cv_has_staff_review = cv_has_staff_review
        self.cv_id = cv_id
        self.cv_image = cv_image
        self.cv_issue_number = cv_issue_number
        self.cv_location_credits = cv_location_credits
        self.cv_name = cv_name
        self.cv_object_credits = cv_object_credits
        self.cv_person_credits = cv_person_credits
        self.cv_site_detail_url = cv_site_detail_url
        self.cv_store_date = cv_store_date
        self.cv_story_arc_credits = cv_story_arc_credits
        self.cv_team_credits = cv_team_credits
        self.cv_team_disbanded_in = cv_team_disbanded_in
        self.cv_volume = cv_volume


# 4010- &field_list=aliases,api_detail_url,deck,description,id,image,name,site_detail_url
# http://comicvine.gamespot.com/api/publisher/4010-10/?field_list=aliases,api_detail_url,deck,description,id,image,name,site_detail_url&api_key=e6cbdacc454cca5f94c16fe7b98dcc0e7badb996
class publisher_cv:
    def __init__(self,
                 cv_aliases,
                 cv_api_detail_url,
                 cv_deck,
                 cv_description,
                 cv_id,
                 cv_image,
                 cv_name,
                 cv_site_detail_url):
        self.cv_aliases = cv_aliases
        self.cv_api_detail_url = cv_api_detail_url
        self.cv_deck = cv_deck
        self.cv_description = cv_description
        self.cv_id = cv_id
        self.cv_image = cv_image
        self.cv_name = cv_name
        self.cv_site_detail_url = cv_site_detail_url


#4050 -
class volume_cv:
    def __init__(self,
                 cv_aliases,
                 cv_api_detail_url,
                 cv_characters,
                 cv_concepts,
                 cv_count_of_issues,
                 cv_date_added,
                 cv_date_last_updated,
                 cv_deck,
                 cv_description,
                 cv_first_issue,
                 cv_id,
                 cv_image,
                 cv_issues,
                 cv_last_issue,
                 cv_locations,
                 cv_name,
                 cv_objects,
                 cv_people,
                 cv_publisher,
                 cv_site_detail_url,
                 cv_start_year,
                 cv_version
                 ):

#4005 -
class character_cv:
    def __init__(self,
                 cv_aliases,
                 cv_api_detail_url,
                 cv_deck,
                 cv_description,
                 cv_name,
                 cv_site_detail_url
                 ):

#
class concept_cv:
    def __init__(self,
                 cv_aliases,
                 cv_api_detail_url,
                 cv_deck,
                 cv_description,
                 cv_name,
                 cv_site_detail_url
                 ):


#
class location_cv:
    def __init__(self,
                 cv_aliases,
                 cv_api_detail_url,
                 cv_deck,
                 cv_description,
                 cv_name,
                 cv_site_detail_url
                 ):
class object_cv:
    def __init__(self,
                 cv_aliases,
                 cv_api_detail_url,
                 cv_deck,
                 cv_description,
                 cv_name,
                 cv_site_detail_url
                 ):
class person_cv:
    def __init__(self,
                 cv_aliases,
                 cv_api_detail_url,
                 cv_deck,
                 cv_description,
                 cv_name,
                 cv_site_detail_url
                 ):
class story_arc_cv:
    def __init__(self,
                 cv_aliases,
                 cv_api_detail_url,
                 cv_deck,
                 cv_description,
                 cv_name,
                 cv_site_detail_url
                 ):
class team_cv:
    def __init__(self,
                 cv_aliases,
                 cv_api_detail_url,
                 cv_deck,
                 cv_description,
                 cv_name,
                 cv_site_detail_url
                 ):







