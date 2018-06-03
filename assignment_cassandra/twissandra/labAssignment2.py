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
         drop keyspace if exists assignment2
         """)

        log.info("creating keyspace...")
        session.execute("""
            CREATE KEYSPACE assignment2
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
            """)

        log.info("setting keyspace...")
        # create tables
        session.set_keyspace("assignment2")

        session.execute("""
                                    CREATE TABLE tweetsmentionhash(
                                    date ascii,
                                    freq int,
                                    hashkey text,
                                    mention text,
                                    PRIMARY KEY (date,freq,hashkey,mention)
                                    ) with clustering order by  (freq desc,hashkey ASC,mention ASC )
                                    """)

        tweetPrepare = session.prepare('insert into tweetsmentionhash JSON ?')
        print('All done!')
        return tweetPrepare

    def load_json(self, tw, tweet_dict):
        log.info("Inserting into tweetsmentionhash keyspace ... ")
        session.execute(tw, [json.dumps(tweet_dict, indent=4, sort_keys=True, default=str)])
