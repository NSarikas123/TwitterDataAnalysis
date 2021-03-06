import re, collections
from django.shortcuts import render, redirect
from django.http import HttpResponse
from dataAnalysis.models import TweetData

#The home directory
def home(request):
    #User Description Hashtags data
    userDescriptionWordsSet = getUsersDescription()
    userDescriptionWordsCount = countWords(userDescriptionWordsSet)
    userDescriptionWordsCount = splitData(userDescriptionWordsCount)

    #Retweet Data
    retweetUserSet = getRetweetedUsers(False)
    retweetUserCount = countWords(retweetUserSet)
    retweetUserCount = splitData(retweetUserCount)

    #Retweet Data without trump
    retweetUserSetNoTrump = getRetweetedUsers(True)
    retweetUserCountNoTrump = countWords(retweetUserSetNoTrump)
    retweetUserCountNoTrump = splitData(retweetUserCountNoTrump)

    #All tweet data
    allTweetedWords = getTweetedWords()
    tweetWordCounts = countWords(allTweetedWords)
    tweetWordCounts = splitData(tweetWordCounts)

    allTweets = getTweets()
    tweetCount = countWords(allTweets)
    tweetCount = splitData(tweetCount)

    #Hashtags used in user descriptions
    allHashTags = getHashTags()
    hashtagCounts = countWords(allHashTags)
    hashtagCounts = splitData(hashtagCounts)

    #All links included in tweets
    allLinks = getHyperLinks()
    linksCounts = countWords(allLinks)
    linksCounts = splitData(linksCounts)

    #The data that will be passed through into the front end
    data = {
        'retweetUserCount' : retweetUserCount,
        'tweetWordCounts' : tweetWordCounts,
        'userDescriptionWordsCount' : userDescriptionWordsCount,
        'retweetUserCountNoTrump' : retweetUserCountNoTrump,
        'hashtagCounts' : hashtagCounts,
        'linksCounts' : linksCounts,
        'tweetCount' : tweetCount
    }
    return render(request,'home.html',data)

#Gets all the users that were retweeted from the database
#an option to exlude trump is also implemented
#returns each word as a list
def getRetweetedUsers(excludeTrump):
    query = TweetData.objects.all().values('retweetedUser')
    querySet = []
    for i in query:
        currentRetweetedUser = i.get('retweetedUser')
        if excludeTrump == False:
            querySet.append(currentRetweetedUser)
        if currentRetweetedUser != "@realDonaldTrump" and excludeTrump == True:
            querySet.append(currentRetweetedUser)
    return querySet

#Gets all tweets from the database and returns each word as a list
def getTweetedWords():
    query = TweetData.objects.all().values('tweetText')
    querySet = []
    #Blacklist of common words that were not needed
    blacklist= ["to","RT","the","from","the","but","at","their","your","know"]
    for i in query:
        #i is string, split() splits the string into a list of words
        eachWord = i.get('tweetText').split()
        for j in eachWord:
            #Removing selected punctuation
            word = j.replace('"','')
            word = word.replace(',','')
            word = word.replace('?','')
            word = word.replace('&','')
            word = word.replace('(','')
            word = word.replace(')','')
            word = word.replace(':','')
            if j not in blacklist:
                querySet.append(word)
    return querySet

def getTweets():
    query ='select * from "dataAnalysis_tweetdata"'
    querySet = []
    for i in TweetData.objects.raw(query):
        querySet.append(i.tweetText)
    return querySet

#Gets every word from the Users Description from the database and returns each word as a list
def getUsersDescription():
    #Blacklist for words User Desciptions
    blacklist = ["and","the","of","to","I","a","&","in","for","my","is","are","with","on","??","????","not","-","our","by","|","you","The","be","all","who","that","at","from","am","A","I'm"]
    queryset = TweetData.objects.all().values('userDescription')
    eachWord = []
    for i in queryset:
        eachUserDescription = i.get('userDescription')
        if eachUserDescription is not None and eachUserDescription != '':
            eachWordInDescription = eachUserDescription.split()
            for j in eachWordInDescription:
                if j not in blacklist:
                    eachWord.append(j)
    return eachWord

#Counts how many times each word occurs
#returns (word, frequency) as sorted tuple decending by frequency
def countWords(tweetedWords):
    wordInfo = collections.OrderedDict()
    for i in range(len(tweetedWords)):
        tweetWord = tweetedWords[i]
        if tweetWord != None:
            tweetWord = tweetWord.replace(',',' ')
        if tweetWord != 'NULL':
            if tweetWord in wordInfo:
                wordInfo[tweetWord] += 1
            else:
                wordInfo[tweetWord] = 1
    sortedDict = sorted(wordInfo.items(), key=lambda x:x[1],reverse=True)
    return sortedDict


#Gets all hashtags in userDescription
#Returns a list of all the hashtags mentioned
def getHashTags():
    query = TweetData.objects.all().values('userDescription')
    querySet = []
    for i in query:
        eachUserDescription = i.get('userDescription')
        if eachUserDescription is not None and eachUserDescription != '':
            eachWord = eachUserDescription.split()
            for j in eachWord:
                hashtags = re.findall(r"#\w+", j)
                if hashtags:
                    querySet.append(hashtags[0])
    return querySet

#Gets all hyperlinks mentioned in user desciptions
#Returns all the links in a list
def getHyperLinks():
    query = TweetData.objects.all().values('userDescription')
    querySet = []
    for i in query:
        eachUserDescription = i.get('userDescription')
        if eachUserDescription is not None and eachUserDescription != '':
            eachWord = eachUserDescription.split()
            for j in eachWord:
                #Some regular expression to get both https and http links
                hyperlinkHTTPS = re.findall("https:+.*",j)
                hyperlinkHTTP = re.findall("http:+.*",j)
                if hyperlinkHTTPS:
                    querySet.append(hyperlinkHTTPS[0])
                if hyperlinkHTTP:
                    querySet.append(hyperlinkHTTP[0])
    return querySet

#Returns a shortened amount of data, used because queried data returns too many entries
def splitData(data):
    cutData = data[0:9]
    return cutData
