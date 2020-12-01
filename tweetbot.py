import tweepy

API_key = "WBrAwupipZTIPiRikJMwyeAFO"

API_SECRET = "pLx3lKl4KP91GN93ITEDCxG1Gt1ocMRfCXTuR1xDJhXJW97jay"

Access_token = "439057356-XVxTodCTpQ7wVNxKmkBC5eyowjwIeOlTWPC2tkwz"

Access_token_secret = "o2K6Qk7qi2H9AIPDuGV6bNgpta40jGTmD7W5E3y2NIwx9"

auth = tweepy.OAuthHandler(API_key , API_SECRET)

auth.set_access_token(Access_token,Access_token_secret)


api = tweepy.API(auth)

public_tweets = api.trends_place(id=23424848)
print(type(public_tweets))
for tweet in public_tweets:
    #print(tweet.values())
    a = tweet.values()
    print(list(a)[0][0]['name'])