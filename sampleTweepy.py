#!/usr/bin/env python
""" -*- coding: utf-8 -*-
Usage from command prompt is $python sampleTweepy.py or
$python sampleTweepy.py > [outputfile] to write to an output file.

Github and sample code that was the basis of this implementation.
https://github.com/tweepy/tweepy/tree/master/tweepy
http://h6o6.com/2012/12/mining-the-public-tweet-stream-for-fun-and-profit/ 

This implementation uses the tweepy package for help in authorization and
parsing of the tweet stream.  StreamWatcherHandler inherits from StreamListener
and overrides two of its methods for processing the tweets.  The method on_status
read and parses the tweet and then writes the output to stdout.  Within main, the 
authentication tokens are set and then the stream object is called to retrieve
the stream from the twitter endpoint at https://stream.twitter.com/1.1/statuses/sample.json.

"""

import tweepy
 
class StreamWatcherHandler(tweepy.StreamListener):
    """ Handles all incoming tweets as discrete tweet objects.
        This class overrides the on_status and on_error methods
        In order to process the tweet object as is preferred.
    """
 
    def on_status(self, status):
        """Called when status (tweet) object received.
        See the following link for more information:
        https://github.com/tweepy/tweepy/blob/master/tweepy/models.py
        """
        try:
            #Get the tweet time, follower count and length of user mention
            #from the tweet object, print it (to stdout)
            #Tweet time is in UTC time.
            tweet_time = status.created_at
            followers = status.user.followers_count
            usr_mentions = len(status.entities['user_mentions'])
            #Could insert a function here that would write it to a file.
            print str(tweet_time) + "," + str(followers) + "," + str(usr_mentions) 
           
        except Exception as e:
            # Most errors relate to the handling of UTF-8 messages
            print(e)
 
    def on_error(self, status_code):
       #print('An error has occured! Status code = %s' % status_code)
       return True
 
def main():
    # establish stream, set the consumer_key and consumer_secret
    consumer_key = "<USER KEY HERE>"
    consumer_secret = "USER SECRET HERE"
    auth1 = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    
    # set the access_token and access_token_secret
    access_token = "<ACCESS TOKEN HERE>"
    access_token_secret = "<ACCESS TOKEN SECRET HERE>"
    auth1.set_access_token(access_token, access_token_secret)
    
    # create the stream object with the authorization and our StreamWatchedHandler
    stream = tweepy.Stream(auth1, StreamWatcherHandler(), timeout=None)
 
    # Start pulling our sample streaming API from Twitter to be handled by StreamWatcherHandler
    stream.sample()
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        #print "Done"
        pass
