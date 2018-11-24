import re
import datetime
import numpy as np


class TweetParser(object):

    def __init__(self):
        self.collector_full_tweet = {"tweet": [],
                                     "tweet_length": [],
                                     "hashtags": [],
                                     "mentions": [],
                                     "is_retweet": [],
                                     "is_retweeted": [],
                                     "retweet_count": [],
                                     "reply_count": [],
                                     "favorite_count": [],
                                     "lang_tweet": [],
                                     "source": [],
                                     "user_name": [],
                                     "user_verified": [],
                                     "user_lang": [],
                                     "user_description": [],
                                     "user_follower_number": [],
                                     "user_friends_number": [],
                                     "user_favorites_count": [],
                                     "user_statuses_count": [],
                                     "user_set_location": [],
                                     "location_city": [],
                                     "location_country": [],
                                     "country_code": [],
                                     "geo_latitude": [],
                                     "geo_longitude": [],
                                     "created": [],
                                     "created_date": [],
                                     "created_min": [],
                                     "created_hour": [],
                                     "created_day": [],
                                     "created_month": [],
                                     "created_year": [],
                                     }
        self.collector_tweet_data = {"tweet": [],
                                     "tweet_length": [],
                                     "hashtags": [],
                                     "mentions": [],
                                     "is_retweet": [],
                                     "is_retweeted": [],
                                     "retweet_count": [],
                                     "reply_count": [],
                                     "favorite_count": [],
                                     "lang_tweet": [],
                                     "source": [],
                                     "created": [],
                                     "created_date": [],
                                     "created_year": [],
                                     "created_month": [],
                                     "created_day": [],
                                     "created_hour": [],
                                     "created_min": [],
                                     "user_name": []
                                     }
        self.collector_users_data = {"user_name": [],
                                     "user_verified": [],
                                     "user_lang": [],
                                     "user_description": [],
                                     "user_follower_number": [],
                                     "user_friends_number": [],
                                     "user_favorites_count": [],
                                     "user_statuses_count": [],
                                     "user_set_location": [],
                                     "location_city": [],
                                     "location_country": [],
                                     "country_code": [],
                                     "geo_latitude": [],
                                     "geo_longitude": []
                                     }

    # The following 7 functions return the timestamps/date/year/month/day/hour/minute from a tweet
    @staticmethod
    def created(tweet):
        result = datetime.datetime.fromtimestamp(int(tweet["timestamp_ms"]) / 1000.0)
        return result

    def created_date(self, tweet):
        result = self.created(tweet)
        return result.date()

    def created_year(self, tweet):
        result = self.created(tweet)
        return result.year

    def created_month(self, tweet):
        result = self.created(tweet)
        return result.month

    def created_day(self, tweet):
        result = self.created(tweet)
        return result.day

    def created_hour(self, tweet):
        result = self.created(tweet)
        return result.hour

    def created_minute(self, tweet):
        result = self.created(tweet)
        return result.minute

    #
    @staticmethod
    def source(tweet):
        """
        This function returns the device/client used to send the tweet.
        """
        result = re.split(r"(>|<)", tweet["source"])[4]
        return result

    @staticmethod
    def user_name(tweet):
        result = tweet["user"]["name"]
        return result

    @staticmethod
    def location_user_set(tweet):
        """
        This function returns the location manually set by the user.
        """
        if tweet["user"]["location"]:
            result = tweet["user"]["location"].split(",")
            result = result[0]
            return result

        else:
            return None

    @staticmethod
    def geo_location(tweet):
        """
        Data available only if the user accepted to share its location.
        This function returns the latitude and longitude from where the tweet has been sent.
        """
        result = [None, None]
        if tweet["geo"]:
            result = tweet["geo"]["coordinates"]

        elif tweet["place"]:
            geo_coord = tweet["place"]["bounding_box"]["coordinates"][0]
            longitude = []
            latitude = []

            for coordinate in geo_coord:
                longitude.append(coordinate[0])
                latitude.append(coordinate[1])

            result = [np.average(latitude), np.average(longitude)]

        return result

    @staticmethod
    def location_city(tweet):
        """
        This data is usually available when the geolocation is enabled.
        """
        result = None
        if tweet["place"]:
            result = tweet["place"]["name"]
            return result
        return result

    @staticmethod
    def location_country(tweet):
        """
        This data is usually available when the geolocation is enabled.
        """
        if tweet["place"]:
            result = tweet["place"]["country"]
            return result

        else:
            return None

    @staticmethod
    def location_country_code(tweet):
        """
        This data is usually available when the geolocation is enabled.
        """
        result = None
        if tweet["place"]:
            result = tweet["place"]["country_code"]
            return result
        return result

    @staticmethod
    def tweet_text(tweet):
        if "extended_tweet" in tweet.keys():
            return tweet["extended_tweet"]["full_text"]

        else:
            return tweet["text"]

    def tweet_length(self, tweet):
        result = len(self.tweet_text(tweet))
        return result

    @staticmethod
    def mentions(tweet):
        if len(tweet["entities"]["user_mentions"]) != 0:
            result = []
            for mention in tweet["entities"]["user_mentions"]:
                result.append(mention["screen_name"])
            return ",".join(result)

        else:
            return None

    def is_retweet(self, tweet):
        """
        All the tweets that has been retweeted starts with "RT", exploiting this constant this function check
        if the input is either a retweet or not.
        """
        if "RT" == self.tweet_text(tweet)[0:2]:
            return True

        else:
            return False

    @staticmethod
    def is_retweeted(tweet):
        """
        This function check if the tweet has been retweeted by some other users.
        """
        if tweet["retweeted"] == True:
            return True

        else:
            return False

    @staticmethod
    def retweet_count(tweet):
        result = int(tweet["retweet_count"])
        return result

    @staticmethod
    def reply_count(tweet):
        result = int(tweet["reply_count"])
        return result

    @staticmethod
    def favorite_count(tweet):
        result = int(tweet["favorite_count"])
        return result

    @staticmethod
    def hashtags(tweet):
        if len(tweet["entities"]["hashtags"]) != 0:
            result = []
            for hashtag in tweet["entities"]["hashtags"]:
                result.append(hashtag["text"])
            return ",".join(result)

        else:
            return None

    @staticmethod
    def lang_tweet(tweet):
        """
        This function returns the language of the tweet.
        """
        result = tweet["lang"]
        return result

    @staticmethod
    def lang_user(tweet):
        """
        This function returns the language set by the user in its profile.
        """
        result = tweet["user"]["lang"]
        return result

    @staticmethod
    def user_follower(tweet):
        result = tweet["user"]["followers_count"]
        return result

    @staticmethod
    def user_friends(tweet):
        result = tweet["user"]["friends_count"]
        return result

    @staticmethod
    def user_description(tweet):
        """
        This function returns the description on the user profile.
        """
        result = tweet["user"]["description"]
        return result

    @staticmethod
    def user_verified(tweet):
        """
        This function returns if the user is either verified or not.
        """
        result = tweet["user"]["verified"]
        return result

    @staticmethod
    def user_favorites_count(tweet):
        """
        This function returns the total number of favourites tweet of the user.
        """
        result = int(tweet["user"]["favourites_count"])
        return result

    @staticmethod
    def user_statuses_count(tweet):
        """
        This function returns the total number of the statuses sent by the user.
        """
        result = int(tweet["user"]["statuses_count"])
        return result

    @staticmethod
    def account_creation_date(tweet):
        """
        This function returns when the user's account has been created.
        """
        result = tweet["user"]["created_at"]
        return result

    def __tweet_dict(self, tweet):
        result = {"tweet": self.tweet_text(tweet),
                  "tweet_length": self.tweet_length(tweet),
                  "hashtags": self.hashtags(tweet),
                  "mentions": self.mentions(tweet),
                  "is_retweet": self.is_retweet(tweet),
                  "is_retweeted": self.is_retweeted(tweet),
                  "retweet_count": self.retweet_count(tweet),
                  "reply_count": self.reply_count(tweet),
                  "favorite_count": self.favorite_count(tweet),
                  "lang_tweet": self.lang_tweet(tweet),
                  "source": self.source(tweet),
                  "created": self.created(tweet),
                  "created_date": self.created_date(tweet),
                  "created_year": self.created_year(tweet),
                  "created_month": self.created_month(tweet),
                  "created_day": self.created_day(tweet),
                  "created_hour": self.created_hour(tweet),
                  "created_min": self.created_minute(tweet),
                  "user_name": self.user_name(tweet)
                  }

        return result

    def tweet_data_only(self, t_input, output_type="dict"):
        """
        This functions takes as an input a tweet or a collection of tweets and returns the most valuable information about it.
        :param t_input: tweet - dict type / tweets - iterable
        :param output_type: user can select the data type of the output: dict / tuple with only the values
        :return: a dict or a tuple with the most valuable info about the tweet/tweets but not the info
        about the user.
        """
        if type(t_input) is dict:
            result = self.__tweet_dict(t_input)

            if output_type == "dict":
                return result
            elif output_type == "tuple":
                return tuple(result.values())
            else:
                raise ValueError("output_type is not valid, use 'dict' or 'tuple'")

        elif type(t_input) is list or type(t_input) is tuple:
            for tweet in t_input:
                result = self.__tweet_dict(tweet)
                for key in result.keys():
                    self.collector_tweet_data[key].append(result[key])

            if output_type == "dict":
                return self.collector_tweet_data
            elif output_type == "tuple":
                return tuple(self.collector_tweet_data.values())
            else:
                raise ValueError("output_type is not valid, use 'dict' or 'tuple'")

        else:
            raise TypeError("input is not valid, try 'dict','list' or 'tuple'")

    def __user_dict(self, tweet):
        result = {"user_name": self.user_name(tweet),
                  "user_verified": self.user_verified(tweet),
                  "user_lang": self.lang_user(tweet),
                  "user_description": self.user_description(tweet),
                  "user_follower_number": self.user_follower(tweet),
                  "user_friends_number": self.user_friends(tweet),
                  "user_favorites_count": self.user_favorites_count(tweet),
                  "user_statuses_count": self.user_statuses_count(tweet),
                  "user_set_location": self.location_user_set(tweet),
                  "location_city": self.location_city(tweet),
                  "location_country": self.location_country(tweet),
                  "country_code": self.location_country_code(tweet),
                  "geo_latitude": self.geo_location(tweet)[0],
                  "geo_longitude": self.geo_location(tweet)[1],
                  "user_account_creation": self.account_creation_date(tweet)
                  }

        return result

    def user_data_only(self, t_input, output_type="dict"):
        """
        This functions takes as an input a tweet or a collection of tweets and returns the most valuable information
        about the user.
        :param t_input: tweet - dict type / tweets - iterable
        :param output_type: user can select the data type of the output: dict / tuple with only the values
        :return: a dict or a tuple with the most valuable values related to the user/users.
        """
        if type(t_input) is dict:
            result = self.__user_dict(t_input)

            if output_type == "dict":
                return result
            elif output_type == "tuple":
                return tuple(result.values())
            else:
                raise ValueError("output_type is not valid, use 'dict' or 'tuple'")

        elif type(t_input) is list or type(t_input) is tuple:
            for tweet in t_input:
                result = self.__user_dict(tweet)
                for key in result.keys():
                    self.collector_users_data[key].append(result[key])

            if output_type == "dict":
                return self.collector_users_data
            elif output_type == "tuple":
                return tuple(self.collector_users_data.values())
            else:
                raise ValueError("output_type is not valid, use 'dict' or 'tuple'")

        else:
            raise TypeError("input is not valid, try 'dict','list' or 'tuple'")

    def __full_tweet_dict(self, tweet):
        """
        This function merges the value returned by the functions '__tweet_dict()' and '__user_dict(tweet)' into
        a dict.
        """
        result = {**self.__tweet_dict(tweet), **self.__user_dict(tweet)}
        return result

    def full_tweet_data(self, t_input, output_type="dict"):
        """
        This functions takes in a tweet or a collection of tweets and returns the most valuable info about the
        tweet/tweets and the user/users.
        :param t_input: tweet - dict type / tweets - iterable
        :param output_type: user can select the data type of the output: dict / tuple with only the values
        :return: a dict or a tuple with all the most valuable info.
        """
        if type(t_input) is dict:
            result = self.__full_tweet_dict(t_input)

            if output_type == "dict":
                return result
            elif output_type == "tuple":
                return tuple(result.values())
            else:
                raise ValueError("output_type is not valid, use 'dict' or 'tuple'")

        elif type(t_input) is list or type(t_input) is tuple:
            for tweet in t_input:
                result = self.full_tweet_data(tweet)
                for key in result.keys():
                    self.collector_full_tweet[key].append(result[key])

            if output_type == "dict":
                return self.collector_full_tweet
            elif output_type == "tuple":
                return tuple(self.collector_full_tweet.values())
            else:
                raise ValueError("output_type is not valid, use 'dict' or 'tuple'")

        else:
            raise TypeError("input is not valid, try 'dict','list' or 'tuple'")
