import csv,os,codecs
from dataAnalysis.models import TweetData

with codecs.open('tweetData.csv','r',encoding='utf-8',errors='ignore') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tweetRow = TweetData(tweetText=row['Tweet Text'],userDescription=row['User Description'],userFollowersCount=row['User Followers Count'],userFriendsCount=row['UserFriends Count'],inReplytoUserID=row['In Reply to User ID'],userLocation=row['User Location'],retweetCount=row['Retweet Count'],tweetLanguage=row['Tweet Language'],tweetedBy=row['Tweeted By'],originalTweetUserID=row['Original Tweet User ID'],originalTweetFriendsCount=row['Original Tweet Friends Count'],originalTweetFollowersCount=row['Original Tweet Followers Count'],originalTweetRTCount=row['Original Tweet RT Count'],retweetedUser=row['Retweeted User'])
        tweetRow.save()
