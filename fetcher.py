from tweepy import OAuthHandler, Cursor, API, TweepError

from settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET
import json

consumer_key = CONSUMER_KEY
consumer_secret = CONSUMER_SECRET
access_token = ACCESS_TOKEN
access_secret = ACCESS_SECRET

class Fetcher():
    def __init__(self, with_access_token=True):
        self.auth = OAuthHandler(consumer_key, consumer_secret)

        if with_access_token:
            print('ya')
            self.auth.set_access_token(access_token, access_secret)

        self.api = API(self.auth)

    # search by q = keyword, geocode and language
    def search(self, keyword, geocode):
        tweets = []
        tweet_id_flag = set()
        # change items
        cursor = Cursor(self.api.search, q=keyword, geocode=geocode, lang='id', tweet_mode='extended').items(10)
        while True:
            try:
                status = cursor.next()
                if status.id in tweet_id_flag:
                    continue
                tweet_id_flag.add(status.id)

                tweets.append({
                    'id': status.id,
                    'full_text': status.full_text,
                    'retweet_count': status.retweet_count,
                })
                print({
                    'id': status.id,
                    'full_text': status.full_text,
                    'retweet_count': status.retweet_count,
                })
            except TweepError as err:
                print(err)
                continue
            except StopIteration:
                break
        return tweets

    # search by user_name
    def search_by_user(self, user_name):
        user = self.api.get_user(screen_name=user_name)
        cursor = Cursor(self.api.user_timeline, user_id=user.id, tweet_mode='extended').items(1)
        tweets = []
        tweet_id_flag = set()
        for i in range(0, 1):
            try:
                status = cursor.next()
                if status.id in tweet_id_flag:
                    continue
                tweet_id_flag.add(status.id)
                
                print(status)

                tweets.append({
                    'id': status.id,
                    'full_text': status.full_text,
                    'retweet_count': status.retweet_count,
                })
                print({
                    'id': status.id,
                    'full_text': status.full_text,
                    'retweet_count': status.retweet_count,
                })
            except StopIteration:
                break
        
        return tweets

def main():
    fetcher = Fetcher()
    # fetcher.search('corona', '-6.227193,106.808098,10km')
    fetcher.search_by_user('FiersaBesari')

if __name__ == '__main__':
    main()