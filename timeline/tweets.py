""" prints the twitter timeline of a user """

from sys import argv
from histogram import histogram, inv_dict, most_freq, sort_dct
from utils import ununicode, unescape, parser, get_hashtags, \
            get_mentions, get_tweets, get_tweet


def remove_self(mentions, scr_name):
    """ removes mention of scr_name """
    return [mention for mention in mentions if not scr_name in mention]


def extract_tweets(tweets, cmd_line=False):
    """ prints the tweets from tweets: list of tweet dicts """
    tweet_texts = []
    for tweet in tweets:
        text = get_tweet(tweet)
        if cmd_line:
            text = text.encode('unicode-escape')
            text = ununicode(text)
            text = unescape(text)
        tweet_texts.append(parser(text))
    return tweet_texts


def print_stats(stat_lst, count=2):
    """ prints count number of stats:list of tuples
        of the form (data, count)
    """
    if len(stat_lst) == 0:
        print 'Empty: No stats available!'
    else:
        if len(stat_lst) < count:
            count = len(stat_lst)
            print 'there is only', count, 'stats'

        idx = 0
        for dummy_ in range(count):
            print stat_lst[idx][0],  stat_lst[idx][1]
            idx += 1
    print

from utils import strings_startswith

def get_hash_mentions(tweets, count=3):
    """ returns stats about hashtags and mentions from tweets
        tweets: a list of strings
    """
    hashtags = strings_startswith(tweets, '#')
    mentions = strings_startswith(tweets, '@')
    freq_hashtags =  sort_dct(histogram(hashtags))
    freq_mentions =  sort_dct(histogram(mentions))
    return freq_hashtags[:count], freq_mentions[:count]
    

def get_stats(tweets, scr_name, count=2):
    """ returns stats about hashtags and user mentions 
        tweets: a dict of tweet dicts from rest api
    """
    hashtags = get_hashtags(tweets)
    mentions = get_mentions(tweets)
    
    freq_hashtags =  sort_dct(histogram(hashtags))
    freq_mentions =  sort_dct(histogram(mentions))
    freq_mentions = remove_self(freq_mentions, scr_name)
    return freq_hashtags[:count], freq_mentions[:count]

def main():
    """ prints timeline  and stats"""
    if len(argv) != 4:
        print 'usage: tweets.py screen_name tweet_count stat_count'
        return
    scr_name = argv[1]
    twt_count, stat_count = int(argv[2]), int(argv[3])
    tweets = get_tweets(scr_name, twt_count)
    #print extract_tweets(tweets)
    print len(tweets), 'tweets displayed'
    tags, mentions = get_stats(tweets, scr_name, stat_count)
    print_stats(tags, stat_count)
    print_stats(mentions, stat_count)

if  __name__ == '__main__':
    main()
