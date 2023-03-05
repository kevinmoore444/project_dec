from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model
import re

class Adventure:
    def __init__(self,data):
        self.id = data['id']
        self.route_name = data['route_name']
        self.location = data['location']
        self.activity_type = data['activity_type']
        self.activity_distance = data['activity_distance']
        self.vertical_elevation = data['vertical_elevation']
        self.terrain_type = data['terrain_type']
        self.route_logistics = data['route_logistics']
        self.gpx_link = data['gpx_link']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

# Get all Methods used to render the dashboard home page

    @classmethod
    def get_all_running(cls):
        query = """
            SELECT * FROM adventures
            JOIN users ON adventures.user_id = users.id
            WHERE activity_type = "Running"
            ORDER BY activity_distance DESC
        """
        results = connectToMySQL(DATABASE).query_db(query)
        all_running_adventures = []
        if results:
            for row in results:
                this_running_adventure = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                }
                this_user = user_model.User(user_data)
                this_running_adventure.reporter = this_user
                all_running_adventures.append(this_running_adventure)
        return all_running_adventures


    @classmethod
    def get_all_biking(cls):
        query = """
            SELECT * FROM adventures
            JOIN users ON adventures.user_id = users.id
            WHERE activity_type = "Biking"
            ORDER BY activity_distance DESC
        """
        results = connectToMySQL(DATABASE).query_db(query)
        all_biking_adventures = []
        if results:
            for row in results:
                this_biking_adventure = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                }
                this_user = user_model.User(user_data)
                this_biking_adventure.reporter = this_user
                all_biking_adventures.append(this_biking_adventure)
        return all_biking_adventures

# Function invoked to post a new adventure on post.html.

    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO adventures (activity_type, route_name, location, activity_distance, vertical_elevation, terrain_type, route_logistics, gpx_link, user_id)
            VALUES (%(activity_type)s,%(route_name)s,%(location)s,%(activity_distance)s,%(vertical_elevation)s,%(terrain_type)s,%(route_logistics)s,%(gpx_link)s, %(user_id)s)
        """
        return connectToMySQL(DATABASE).query_db(query,data)

# Function invoked to delete an adventure

    @classmethod
    def delete(cls,data):
        query = """
        DELETE FROM adventures 
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

# Function invoked to update an adventure

    @classmethod
    def update(cls,data):
        query = """
            UPDATE adventures
            SET activity_type = %(activity_type)s, route_name = %(route_name)s, 
            location = %(location)s, activity_distance = %(activity_distance)s,
            vertical_elevation = %(vertical_elevation)s, terrain_type = %(terrain_type)s,
            route_logistics = %(route_logistics)s, gpx_link = %(gpx_link)s
            WHERE adventures.id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

# Function invoked to pull one adventure in order to view or update.

    @classmethod
    def get_one_adventure(cls,data):
        query = """
            SELECT * FROM adventures JOIN users
            ON users.id = adventures.user_id
            WHERE adventures.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:    
            one_adventure = cls(results[0])
            row = results[0]
            user_data = {
                    **row,
                    "id" : row['users.id'],
                    "created_at" : row['users.created_at'],
                    "updated_at" : row['users.updated_at'],
            }
            user_instance = user_model.User(user_data)
            one_adventure.reporter = user_instance
            return one_adventure
        return False

# Function to validate the post or edit features.

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['activity_type']) < 1:
            flash("Must select activity type!")
            is_valid = False
        if len(form_data['route_name']) < 1:
            flash("Route name must be at least three characters!")
            is_valid = False
        if len(form_data['location']) < 1:
            flash("Must select location!")
            is_valid = False
        if len(form_data['activity_distance']) < 1:
            flash("Must include activity distance!")
            is_valid = False
        elif int(form_data['activity_distance']) < 1:
            flash("Distance must be 1 mile or more!")
            is_valid = False
        if len(form_data['vertical_elevation']) < 1:
            flash("Must include vertical elevation!")
            is_valid = False
        elif int(form_data['vertical_elevation']) < 1:
            flash("Vertical Elevation must be 1 ft. or more!")
            is_valid = False
        if len(form_data['terrain_type']) < 1:
            flash("Must include terrain type!")
            is_valid = False
        if len(form_data['gpx_link']) < 5:
            flash("Must include link to the GPX file!")
            is_valid = False
        return is_valid

    