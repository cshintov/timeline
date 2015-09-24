from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from tweets import extract_tweets, get_tweets, get_stats, remove_self


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
    tweets = get_tweets(scr_name, twt_count)
    if 'error' in tweets:
        retry = '<br><a href="/timeline/get_input">Try another user!</a>'
        return HttpResponse(tweets['error'] + retry)
    hash_tags, mentions = get_stats(tweets, scr_name, stat_count)
    mentions = remove_self(mentions, scr_name)
    tweets = extract_tweets(tweets)
    return result(request, tweets, hash_tags, mentions)

