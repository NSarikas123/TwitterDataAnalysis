from django.db import models

# Create your models here.
class TweetData(models.Model):
    tweetText = models.CharField(max_length=1000, default=None,null=True, blank=True)
    userDescription = models.CharField(max_length=1000,  default=None,null=True, blank=True)
    userFollowersCount =models.CharField(max_length=1000, default=None,null=True, blank=True)
    userFriendsCount = models.CharField(max_length=1000,  default=None,null=True, blank=True)
    inReplytoUserID = models.CharField(max_length=1000, default=None,null=True, blank=True)
    userLocation = models.CharField(max_length=1000, default=None,null=True, blank=True)
    retweetCount = models.CharField(max_length=1000, default=None,null=True, blank=True)
    tweetLanguage = models.CharField(max_length=1000, default=None,null=True, blank=True)
    tweetedBy = models.CharField(max_length=1000, default=None,null=True, blank=True)
    originalTweetUserID = models.CharField(max_length=1000, default=None,null=True, blank=True)
    originalTweetFriendsCount = models.CharField(max_length=1000, default=None,null=True, blank=True)
    originalTweetFollowersCount = models.CharField(max_length=1000, default=None,null=True, blank=True)
    originalTweetRTCount = models.CharField(max_length=1000, default=None,null=True, blank=True)
    retweetedUser = models.CharField(max_length=1000, default=None,null=True, blank=True)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class GraphImage(models.Model):
    image = models.ImageField(upload_to=user_directory_path ,blank=True, null=True)
