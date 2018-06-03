import os
import json

from labAssignment2 import DBnoSQL
from datetime import datetime

keyspaces = DBnoSQL()
tprep = DBnoSQL.create_schema(keyspaces)

path = 'workshop_dataset1'
filelist = os.listdir(path)
tweet_dict = {}
# keyspaces.create_view()
for i in filelist:
    with open(path + "/" + str(i)) as data_file:
        data = json.load(data_file)
        for k, v in data.items():
            if v['hashtags']:
                for e in v['hashtags']:
                    if v['mentions']:
                        for m in v['mentions']:
                            tweet_dict[(str(v['date']), (e, m))] = tweet_dict.get((str(v['date']), (e, m)), 0) + 1

print(tweet_dict)

for a, b in tweet_dict:
    print(a)
    t,y = b
    temp = {'date': a, 'freq': int(tweet_dict[(a, b)]), 'hashkey': t, 'mention':y}
    keyspaces.load_json(tprep, temp)
