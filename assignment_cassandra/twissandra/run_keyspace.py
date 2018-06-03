import os
import json

from sync_cassandra import DBnoSQL
from datetime import datetime

keyspaces = DBnoSQL()
tprep, tprephash, tprepkey, tprepmention, tprepdate, tprepfreq, tpreploc = DBnoSQL.create_schema(keyspaces)

path = 'workshop_dataset1'
filelist = os.listdir(path)
hashmap = {}
hash_counter = {}
# keyspaces.create_view()
for i in filelist:
    with open(path + "/" + str(i)) as data_file:
        data = json.load(data_file)
        for k, v in data.items():
            tweet_dict = {}
            freq_dict = {}
            tweet_dict['tid'] = int(k)
            tweet_dict['tweet_text'] = v['tweet_text']
            td = datetime.strptime(v['datetime'], "%Y-%m-%d %H:%M:%S")
            str(td).strip('.')
            tweet_dict['datetime'] = td
            tweet_dict['quote_count'] = int(v['quote_count'])
            tweet_dict['reply_count'] = int(v['reply_count'])
            tweet_dict['like_count'] = int(v['like_count'])
            tweet_dict['retweet_count'] = int(v['retweet_count'])
            if v['hashtags']:
                tweet_dict['hashtags'] = v['hashtags']
            tweet_dict['location'] = v['location']
            tweet_dict['type'] = v['type']
            tweet_dict['lang'] = v['lang']
            if v['keywords_processed_list']:
                tweet_dict['keywords_processed_list'] = v['keywords_processed_list']
            tweet_dict['url_list'] = v['url_list']
            tweet_dict['retweet_source_id'] = v['retweet_source_id']
            if v['mentions']:
                tweet_dict['mentions'] = v['mentions']
            tweet_dict['replyto_source_id'] = v['replyto_source_id']
            tweet_dict['author'] = v['author']
            tweet_dict['author_screen_name'] = v['author_screen_name']
            tweet_dict['author_id'] = int(v['author_id'])
            keyspaces.load_json(tprep, tweet_dict)
            freq_dict['date'] = str(v['date'])
            freq_dict['tid'] = v['tid']
            # populate another table hash
            tweet_dict.pop('hashtags', None)
            if v['hashtags']:
                for e in v['hashtags']:
                    tweet_dict['hashkey'] = e
                    hashmap[(e, v['date'])] = hashmap.get((e, v['date']), 0) + 1
                    keyspaces.load_json(tprephash, tweet_dict)

            tweet_dict.pop('hashkey', None)
            tweet_dict.pop('keywords_processed_list', None)
            if v['keywords_processed_list']:
                for e in v['keywords_processed_list']:
                    if e:
                        tweet_dict['keyWord'] = e
                        keyspaces.load_json(tprepkey, tweet_dict)
            tweet_dict.pop('keyWord', None)
            tweet_dict.pop('mentions', None)

            tweet_dict['date'] = str(v['date'])
            keyspaces.load_json(tprepdate, tweet_dict)
            tweet_dict.pop('date', None)
            if v['location']:
                keyspaces.load_json(tpreploc, tweet_dict)
            if v['mentions']:
                for e in v['mentions']:
                    if e:
                        tweet_dict['mention'] = e
                        keyspaces.load_json(tprepmention, tweet_dict)

for a, b in hashmap:
    temp = {'date': b, 'hashkey': a, 'freq': int(hashmap[(a, b)])}
    keyspaces.load_json(tprepfreq, temp)
