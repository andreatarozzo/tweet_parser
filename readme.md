## Installation

```
#Numpy
Linux: sudo apt-get install python3-numpy
Windows: pip install numpy

#Tweepy
Linux: sudo apt-get install python3-tweepy
Windows: pip install tweepy
```

## Description

This is personal project developed just to mess around a little bit with Tweepy, a library that provides an easy way to 
stream the tweets interacting directly with the TwitterAPI.
I tried to build a parser for the streamed tweets to help me extracting, in a easier way, some
information within the tweets and save them for personal Data Analysis purpose.

* The files in the repository:
    * auth_twitter.py : The place where your authentication keys should be.
    * tweet_stream.py : Used to initialize the stream.
    * keywords.txt : The list of keywords used to filter the tweets from the stream.
    * tweet_parser.py : The actual parser, it handle 'dict' and iterables.
    * tweets_to_sqlite.py : The class used to export the parsed tweets into a simple sqlite db.

## Sources

Some of the code comes from the Tweepy documentation, you can find everything here: 
* [Tweepy Documentation - Getting started](https://tweepy.readthedocs.io/en/v3.5.0/getting_started.html)
* [Tweepy Documentation - Tweets steam](https://tweepy.readthedocs.io/en/v3.5.0/streaming_how_to.html)

For the authentication keys you need to register a twitter developer account:
* [Sign up here](https://developer.twitter.com)
