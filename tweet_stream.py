from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import auth_twitter
import json
from tweets_to_sqlite import TweetToSqlite
from tweet_parser import TweetParser


class StdOutListener(StreamListener):
    """
    Source: https://tweepy.readthedocs.io/en/v3.5.0/streaming_how_to.html
    """

    def __init__(self):
        self.to_db = TweetToSqlite("test_full_tweet", data_to_export="full_tweet")
        self.parser = TweetParser()

    def on_data(self, data):
        try:

            try:
                #converting the data from json format to dict
                converted = json.loads(data)

                #printing the tweet
                print(self.parser.tweet_text(converted))

                #exporting the tweet to db
                self.to_db.export_to_sqlite(converted)
            except KeyError as e:
                print(e)
            return True

        except BaseException as e:
            print(e)

    def on_error(self, status):
        # If 420, too many requests to the server has been made
        print(status)


class TwitterAuth:
    """
    This class handles the auth.
    Source: https://tweepy.readthedocs.io/en/v3.5.0/getting_started.html
    """

    def authenticate(self):
        auth = OAuthHandler(auth_twitter.CONSUMER_KEY, auth_twitter.CONSUMER_SECRET)
        auth.set_access_token(auth_twitter.ACCESS_TOKEN, auth_twitter.ACCESS_TOKEN_SECRET)
        return auth


class TweetStream:
    """
    This class initialize the tweets stream.
    Source: https://tweepy.readthedocs.io/en/v3.5.0/streaming_how_to.html
    """

    def __init__(self):
        self.twitter_auth = TwitterAuth()

    def stream_tweets(self, keywords):
        listener = StdOutListener()
        stream = Stream(auth=self.twitter_auth.authenticate(), listener=listener)
        stream.filter(track=keywords)


if __name__ == "__main__":

    with open("keywords.txt", "r") as f:
        track_words = f.read().split("\n")

    ts = TweetStream()
    ts.stream_tweets(track_words)
