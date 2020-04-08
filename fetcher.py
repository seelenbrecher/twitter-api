from tweepy import OAuthHandler, Cursor, API, TweepError

from settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET
import json
import csv

consumer_key = CONSUMER_KEY
consumer_secret = CONSUMER_SECRET
access_token = ACCESS_TOKEN
access_secret = ACCESS_SECRET

class Fetcher():
    def __init__(self, with_access_token=True):
        self.auth = OAuthHandler(consumer_key, consumer_secret)

        if with_access_token:
            self.auth.set_access_token(access_token, access_secret)

        self.api = API(self.auth)

    # search by q = keyword, geocode and language
    def search(self, keyword, geocode, cnt):
        tweets = []
        tweet_id_flag = set()
        
        # edit params here
        cursor = Cursor(self.api.search, q=keyword, geocode=geocode, lang='id', tweet_mode='extended').items(cnt)

        while True:
            try:
                status = cursor.next()
                if status.id in tweet_id_flag:
                    continue
                tweet_id_flag.add(status.id)

                tweets.append(status)
                print(f'{len(tweets)} tweets collected')
            except TweepError:
                time.sleep(60 * 15)
                continue
            except StopIteration:
                break
        return tweets

    # search by user_name
    def search_by_user(self, user_name, cnt):
        user = self.api.get_user(screen_name=user_name)

        # edit params here
        cursor = Cursor(self.api.user_timeline, user_id=user.id, tweet_mode='extended').items(cnt)

        tweets = []
        tweet_id_flag = set()
        while True:
            try:
                status = cursor.next()
                if status.id in tweet_id_flag:
                    continue
                tweet_id_flag.add(status.id)

                tweets.append(status)
                print(f'{len(tweets)} tweets collected')
            except TweepError:
                time.sleep(60 * 15)
                continue
            except StopIteration:
                break
        
        return tweets

def main():
    fetcher = Fetcher()
    tweets = []
    # geocode format = <lat>,<long>,<radius>
    #tweets = fetcher.search('corona', '-6.227193,106.808098,10km', 10)
    # tweets = fetcher.search_by_user('_zahraul', 10)

    with open('search_result.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        #headers
        csv_writer.writerow(['id', 'userid', 'full_text', 'retweet_count'])

        for tweet in tweets:
            csv_writer.writerow([
                tweet.id,
                tweet.user.id,
                tweet.full_text,
                tweet.retweet_count,
            ])
    

if __name__ == '__main__':
    main()