import os
import sqlite3
from tweet_parser import TweetParser


class TweetToSqlite:

    def __init__(self, file_name, data_to_export="full_tweet"):
        self.parser = TweetParser()
        self.file_name = file_name
        self.data_to_export = data_to_export

    @staticmethod
    def __user_table():
        """
        :return: The query needed to create the 'users'table.
        """
        user_table = "CREATE TABLE users (" \
                     "user_id INTEGER PRIMARY KEY," \
                     "user_name text," \
                     "user_verified int," \
                     "user_lang text," \
                     "user_description text," \
                     "user_followers_number int," \
                     "user_friends_number int," \
                     "user_favorites_count int," \
                     "user_statuses_count int," \
                     "user_set_location text," \
                     "location_city text," \
                     "location_country text," \
                     "country_code text," \
                     "geo_latitude int," \
                     "geo_longitude int," \
                     "user_account_creation text)"

        return user_table

    @staticmethod
    def __tweet_table():
        """
        :return: The query needed to create the 'tweets'table.
        """
        tweet_table = "CREATE TABLE tweets (" \
                      "tweet_id INTEGER PRIMARY KEY," \
                      "tweet text," \
                      "tweet_length int," \
                      "hashtags text," \
                      "mentions text," \
                      "is_retweet int," \
                      "is_retweeted int," \
                      "retweet_count text," \
                      "reply_count int," \
                      "favorite_count int," \
                      "lang_tweet text," \
                      "source text," \
                      "created text," \
                      "created_date text," \
                      "created_year int," \
                      "created_month int," \
                      "created_day int," \
                      "created_hour int," \
                      "created_minute int," \
                      "user_name text)"

        return tweet_table

    def __create_db(self):
        """
        This function create the db, the value of variable 'data_to_export' states which table/tables
        must be created.
        """
        user_table = self.__user_table()
        tweet_table = self.__tweet_table()

        print(self.file_name)
        connection = sqlite3.connect(self.file_name + ".db")
        cursor = connection.cursor()

        if self.data_to_export == "full_tweet":
            cursor.execute(user_table)
            cursor.execute(tweet_table)

        elif self.data_to_export == "user_only":
            cursor.execute(user_table)

        elif self.data_to_export == "tweet_only":
            cursor.execute(tweet_table)

        else:
            raise ValueError("data_choice input is not valid, use 'full_tweet', 'user_only' or 'tweet_only'")

        connection.commit()
        connection.close()

    def __user_values(self, tweet):
        """
        :param tweet: data from the tweets stream
        :return: the user values as a tuple and the query to commit.
        """
        user_values = (self.parser.user_data_only(tweet, output_type="tuple"))
        if len(user_values) == 0:
            return None
        user_query = "INSERT INTO users VALUES (NULL"+",?"*len(user_values)+")"
        return user_values, user_query

    def __tweet_values(self, tweet):
        """
        :param tweet: data from the tweets stream
        :return: the tweet values as a tuple and the query to commit.
        """
        tweet_values = (self.parser.tweet_data_only(tweet, output_type="tuple"))
        if len(tweet_values) == 0:
            return None
        tweet_query = "INSERT INTO tweets VALUES (NULL"+",?"*len(tweet_values)+")"
        return tweet_values, tweet_query

    def __commit_values(self, tweet):
        """
        This function collects the values of the user and/or tweet and commit the values to the db.
        :param tweet: data from the tweets stream
        :return: the tweet values as a tuple and the query to commit.
        """
        connection = sqlite3.connect(self.file_name + ".db")
        cursor = connection.cursor()

        if self.data_to_export == "full_tweet":
            user_values, insert_user_query = self.__user_values(tweet)
            tweet_values, insert_tweet_query = self.__tweet_values(tweet)
            cursor.execute(insert_user_query, user_values)
            cursor.execute(insert_tweet_query, tweet_values)

        elif self.data_to_export == "user_only":
            user_values, insert_user_query = self.__user_values(tweet)
            cursor.execute(insert_user_query, user_values)

        elif self.data_to_export == "tweet_only":
            tweet_values, insert_tweet_query = self.__tweet_values(tweet)
            cursor.execute(insert_tweet_query, tweet_values)

        else:
            raise ValueError("data_choice input is not valid, use 'full_tweet', 'user_only' or 'tweet_only'")

        connection.commit()
        connection.close()

    def export_to_sqlite(self, tweet):
        """
        This function check if a database, with the same name chosen by the user, exists in the folder and if not it
        creates one following the specification about the tables to create.
        After the db is created, the function commits the data to it.
        """
        cwd = os.getcwd()

        if self.file_name + ".db" not in os.listdir(cwd):
            self.__create_db()
            self.__commit_values(tweet)
        else:
            self.__commit_values(tweet)
