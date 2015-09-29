from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from tweets import extract_tweets, get_tweets, get_stats, remove_self
from tweets import get_hash_mentions
from .models import User, Tweet


MAX_TWEET = 3200

def index(request):
    return HttpResponse("Hello, world. You're at timeline site.")


def get_input(request):
    return render(request, 'timeline/get_input.html')


def result(request, tweets, hash_tags, mentions):
    context =  {'tweets': tweets, 'hash_tags': hash_tags, 'mentions': mentions}
    return render(request, 'timeline/result.html', context)


def show_tweets(request):
    scr_name= request.POST.get("screen_name")
    twt_count = int(request.POST.get("tweet_count"))
    stat_count = int(request.POST.get("stat_count"))
    try:
        user = User.objects.get(scr_name=scr_name)
        tweets = [tweet.tweet_text for tweet in user.tweet_set.all()]
        hash_tags, mentions = get_hash_mentions(tweets[:twt_count], stat_count)
        tweets = tweets[:twt_count]
        return result(request, tweets, hash_tags, mentions)
    except User.DoesNotExist:
        tweets = get_tweets(scr_name, MAX_TWEET)
        if 'error' in tweets:
            retry = '<br><a href="/timeline/get_input">Try another user!</a>'
            return HttpResponse(tweets['error']+retry)
        tweets = extract_tweets(tweets)
        user = User(scr_name=scr_name)
        user.save()
        for tweet in tweets:
            user.tweet_set.create(tweet_text=tweet)
        hash_tags, mentions = get_hash_mentions(tweets[:twt_count], stat_count)
    return result(request, tweets[:twt_count], hash_tags, mentions)

