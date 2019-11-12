import csv,operator,re,json,collections,fileinput
import pandas as pandas
import matplotlib.pyplot as plt

def readData():
    file = open("tweetDataStripped.csv","r",encoding="latin-1")
    readData = csv.reader(file, delimiter=',')
    data = []
    for i in readData:
        data.append(i)
    return data

#seperates all tweets words into one list
#0 = tweetText
#1 = User Desciption
#2 = User Follower Count
#3 = User Friends Count
#4 = In Reply to User ID
#5 = User Location
#6 = Retweet Count
def getCollumns(data, collumn):
    allTweets = []
    #allWords = ''
    for i in range(len(data)):
        for j in range(len(data[0])):
            if j == collumn:
                tweetWords = data[i][j].split()
                for k in tweetWords:
                    allTweets.append(k)
    return allTweets


#seperates all tweets into one list
#0 = tweetText
#1 = User Desciption
#2 = User Follower Count
#3 = User Friends Count
#4 = In Reply to User ID
#5 = User Location
#6 = Retweet Count
def getWholeCollumn(data, collumn):
    allTweets = []
    for i in range(len(data)):
        for j in range(len(data[0])):
            if j == collumn:
                allTweets.append(data[i][j])
    return allTweets

#Rewrites column with lowercase characters
def reWriteCollumn(data, collumn):
    for i in range(len(data)):
        for j in range(len(data[0])):
            if j == collumn:
                tweet = data[i][j]
                loweredTweet = tweet.lower()
                formattedTweet = loweredTweet.replace('-','')
                data[i][j] =formattedTweet
    return data

#Counts words and adds to dictionary, sorts in descending order, and returns it
def countWords(tweetedWords):
    wordInfo = collections.OrderedDict()
    for i in range(len(tweetedWords)):
        tweetWord = tweetedWords[i]
        tweetWord = tweetWord.replace(',',' ')
        if tweetWord in wordInfo:
            wordInfo[tweetWord] += 1
        else:
            wordInfo[tweetWord] = 1

    sortedDict = sorted(wordInfo.items(), key=lambda x:x[1],reverse=True)

    return sortedDict


#Searches for all the strings that include the queryString
def queryTweets(tweets, queryString):
    queryString = normalizeString(queryString)
    for i in tweets:
        tweetString = normalizeString(i[0])
        if queryString in tweetString:
            print(tweetString)


#Searches for all the strings that include the queryString
def queryTweetsList(tweets, queryStrings):
    queryString = normalizeString(queryString)
    for i in tweets:
        for j in queryStrings:
            queryString = normalizeString(queryStrings)
            tweetString = normalizeString(i[0])
            if queryString in tweetString:
                print(tweetString)


#Method that changes uppercases to lower, remove - (for now)
def normalizeString(string):
    string = string.lower()
    string = re.sub(r"-"," ",string)
    return string

#Writes a dictionary to a file
def writeDictToFile(dict,location):
    data = json.dumps(dict)
    f = open(location,"w")
    f.write(data)
    f.close()

#Gets all hashtags and returns them
def getHashTags(data):
    hashTags = []
    for i in data:
        if "#" in i:
            hashTags.append(i)
    return hashTags

#Adds retweeted user column to dataset csv
def addRetweetedUserCollumn(tweetData):
    file = pandas.read_csv("tweetDataStrippedTEST.csv",encoding='latin1')
    file['Retweeted User'] = tweetData
    file.to_csv("tweetDataWithRetweets.csv")

#Gets all retweets and returns it as a list
def getAllRetweets(tweetData):
    retweetedUsers = []
    for i in tweetData:
        isRetweet = re.match(r"RT.*?:",i)
        if isRetweet is not None:
            retweetSet = re.findall(r"RT.*?:",i)
            retweet = retweetSet[0]
            retweet = re.sub(r"RT ","",retweet)
            retweet = re.sub(r":.*","",retweet)
            retweetedUsers.append(retweet)
        else:
            retweetedUsers.append("NULL")

    #THIS IS BECAUSE THE TITLE IS BEING LOOKED AT
    retweetedUsers.pop(0)
    return retweetedUsers

#Plots a scatter diagram with data 
def plotBoxPlot(data):
    colors = list("rgbcmyk")
    xValues = []
    yValues = []

    for i in data.items():
        xValues.append(i[0])
        yValues.append(i[1])

    plt.scatter(xValues,yValues,color=colors.pop())
    plt.title('Tweeted Words')
    plt.legend(data.keys())
    plt.savefig("TweetedWords1.png")


#Prints the ordered dictionary (a tuple) to a csv file
def orderedDictToCSV(dictionary,location):
    titleString = "Word,Count\n"
    writeFile = open(location,"a",encoding='latin1')
    writeFile.write(titleString)
    for i in dictionary:
        string = ""
        dataString = str(i[0])+","+str(i[1])+"\n"
        writeFile.write(dataString)
    writeFile.close()

#Alternative write file to csv
def writeNewCSV2(data,location):
    file = fileinput.input(location, openhook=fileinput.hook_encoded("utf-8"))
    for line in file:
        print(line.lower(), end='')

def main():
    #Read all tweet data into list
    data = readData()

    #-----------------TWEET CONTENT-----------------
    #Gets all tweets individual content
    #allTweetedWords = getCollumns(data,0)

    #Prints each word and how many times theyre mentioned across all tweets
    #sortedTweetWords = countWords(allTweetedWords)
    #writeDictToFile(sortedTweetWords,"allTweetedWords.json")

    #orderedDictToCSV(sortedTweetWords,"wordInfo.csv")

    #plotBoxPlot(sortedTweetWords)

    #-----------------USER DESCRIPTION-----------------
    #Gets all users descriptions
    #allUserDescriptions = getCollumns(data,1)
    #Prints out each word in Users Description
    #sortedUserDescriptionWords = countWords(allUserDescriptions)
    #writeDictToFile(sortedUserDescriptionWords,"userDescription.json")
    #orderedDictToCSV(sortedUserDescriptionWords,"userDescriptionWords.csv")

    #-----------------HASH TAGS#-----------------
    #allHashTagsFromDescriptions = getHashTags(allUserDescriptions)
    #hashTagUserDict = countWords(allHashTagsFromDescriptions)
    #writeDictToFile(hashTagUserDict,"userDescriptionHashTags.json")
    #orderedDictToCSV(hashTagUserDict,"userDescriptionHashTags.csv")

    #-----------------RETWEET DATA-----------------
    #allTweets = getWholeCollumn(data,0)
    #allRetweetedUsers = getAllRetweets(allTweets)
    #retweetedUsersCount = countWords(allRetweetedUsers)
    #writeDictToFile(retweetedUsersCount,"retweetedUsers.json")

    #orderedDictToCSV(retweetedUsersCount,"mostRetweets.csv")
    #addRetweetedUserCollumn(allRetweetedUsers)

    #loweredData = reWriteCollumn(data,0)
    #writeNewCSV2(loweredData,"tweetDataWithRetweets.csv")

if __name__ == '__main__':
    main()
