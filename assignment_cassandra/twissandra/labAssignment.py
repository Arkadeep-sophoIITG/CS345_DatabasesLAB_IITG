from cassandra.cluster import Cluster
from datetime import datetime
import json

import logging

log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()


class DBnoSQL:
    def create_schema(self):
        log.info("Dropping keyspace ... ")
        session.execute("""
         drop keyspace if exists assignment
         """)

        log.info("creating keyspace...")
        session.execute("""
            CREATE KEYSPACE assignment
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
            """)

        log.info("setting keyspace...")
        # create tables
        session.set_keyspace("assignment")

        session.execute("""  
            CREATE TABLE tweetsactiveid (
                date ascii,
                freq int,
                author_id bigint,
                PRIMARY KEY (date,freq,author_id)         
            ) WITH clustering ORDER by (freq DESC ,author_id asc)
            """)

        tweetPrepare = session.prepare('insert into tweetsactiveid JSON ?')
        print('All done!')
        return tweetPrepare

    def load_json(self, tw, tweet_dict):
        log.info("Inserting into tweetsactiveid keyspace ... ")
        session.execute(tw, [json.dumps(tweet_dict, indent=4, sort_keys=True, default=str)])
