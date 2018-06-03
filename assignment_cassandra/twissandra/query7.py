from cassandra.cluster import Cluster
from datetime import datetime
import json
import logging
from collections import OrderedDict
import datetime

log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

hash_dict = OrderedDict()


def connect():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.set_keyspace("twissandra")
    return session


def query(session):
    header = ['Tweet id', 'HashKey', 'Text', 'datetime', 'author id', 'user handle', 'location', 'language']
    raw_output = session.execute('select date,hashkey,freq from tweetsTimelinefreq')
    for row in raw_output:
        hash_dict[(row.date, row.hashkey)] = row.freq


def query_output(datea):
    session = connect()
    query(session)
    tweet_hash = {}
    td = datetime.datetime.strptime(datea, '%Y-%m-%d').date()
    date_list = [(td - datetime.timedelta(days=x)).strftime('%Y-%m-%d') for x in range(0, 7)]
    for c, d in hash_dict:
        for date in date_list:
            if d not in tweet_hash:
                tweet_hash[d] = tweet_hash.get(d, 0) + hash_dict.get((date, d), 0)
    tweet_hash = sorted(tweet_hash.items(), key=lambda x: x[1], reverse=True)
    l = []
    print(tweet_hash)
    for a, b in tweet_hash[:20]:
        l.append(a)
    return l
    # return "\n".join(l)


query_output('2017-12-30')
# prepare = "session.prepare('insert into tweetsTimelinefreq JSON ?')"
#
# for a, b in hash_dict:
#     temp = {}
#     log.info("Inserting into tweetsTimeline keyspace ... ")
#     temp = {'date': b, 'hashkey': a, 'freq': int(hash_dict[(a, b)])}
#     session.execute(prepare, [json.dumps(temp, indent=4, sort_keys=True, default=str)])
