from django.db import models


class User(models.Model):
    """ a twitter user handle """
    scr_name = models.CharField(max_length=20)

    def __str__(self):
        return self.scr_name


class Tweet(models.Model):
    """ a user's tweet """
    user = models.ForeignKey(User)
    tweet_text = models.CharField(max_length=200)

    def __str__(self):
        return str(self.user) + ': ' + self.tweet_text
