import os
import json

from labAssignment import DBnoSQL
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
            tweet_dict[(str(v['date']), int(v['author_id']))] = tweet_dict.get((str(v['date']), int(v['author_id'])),
                                                                               0) + 1
print(tweet_dict)

for a, b in tweet_dict:
    temp = {'date': a, 'freq': int(tweet_dict[(a, b)]), 'author_id': int(b)}
    keyspaces.load_json(tprep, temp)
