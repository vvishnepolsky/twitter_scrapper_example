import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

class TwitterClient():

    def __init__(self):
        # Initialize Twitter API

        consumer_key='U9cRqU2b3II7kXOxF1HjDHMFq'
        consumer_secret='7NNp3B3XvgofNbqSsoQpERTJpqxJUupq5csru4vxLwOXPWdi5q'
        access_token_key='879415581543460864-31E3dQz6YHxz6poDccfBwxnfRKcfiWO'
        access_token_secret='mGAQtkwcySX4sFernk5y8rEtmDlOaFNIMV3Vd6ZQg2SQ0'

        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token_key, access_token_secret)
        self.api = tweepy.API(self.auth)
        self.tweets = []

    def sentimentAnalysis(self, text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        if polarity > 0:
            return "positive"
        elif polarity == 0:
            return "neutral"
        else:
            return "negative"

    def getTweets(self, user_id,count):

        unparsed_tweets = self.api.user_timeline(user_id, count = count)

        for tweet in unparsed_tweets:
            parsed_tweet = {}
            parsed_tweet['text'] = tweet.text
            parsed_tweet['polarity'] = self.sentimentAnalysis(tweet.text)

            self.tweets.append(parsed_tweet)

    def polarityAnalysis(self, user_id):

        total = len(self.tweets)
        positive = 0
        negative = 0
        neutral = 0

        for tweet in self.tweets:
            if(tweet['polarity'] == 'positive'):
                positive += 1
            elif(tweet['polarity'] == 'negative'):
                negative += 1
            else:
                neutral += 1

        print("Breakdown of User " + user_id + " Polarity: \n")

        print("Positive tweets percentage: {} %".format(100*positive/total))
        print("Negative tweets percentage: {} %".format(100*negative/total))
        print("Neutral tweets percentage: {} %".format(100*neutral/total))

    def displayPositive(self):
        for tweet in self.tweets:
            if(tweet['polarity'] == 'positive'):
                print(tweet['text'] + "\n")

# Insantiate class

scrapper = TwitterClient()

# Ask for user inputs

user_id = input("Enter the Twitter Handle without @: ")
count = input("How many Tweets do you want to analyze: ")

scrapper.getTweets(user_id, count)
scrapper.polarityAnalysis(user_id)
scrapper.displayPositive()
