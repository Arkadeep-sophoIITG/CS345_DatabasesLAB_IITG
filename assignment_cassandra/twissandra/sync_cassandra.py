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
         drop keyspace if exists twissandra
         """)

        log.info("creating keyspace...")
        session.execute("""
            CREATE KEYSPACE twissandra
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
            """)

        log.info("setting keyspace...")
        # create tables
        session.set_keyspace("twissandra")

        session.execute("""  
            CREATE TABLE tweetsTimeline (
                tid bigint,
                tweet_text text,
                datetime TIMESTAMP ,
                quote_count int,
                reply_count int,
                like_count int,
                retweet_count int,
                hashtags list<text>,
                location text,
                type ascii,
                lang ascii,
                keyWords_processed_list list<text>,
                url_list list<text>,
                retweet_source_id bigint,
                mentions list<text>,
                replyto_source_id bigint,
                author text,
                author_screen_name ascii,
                author_id bigint,
                PRIMARY KEY (author_screen_name,datetime,tid)         
            ) WITH clustering ORDER by (datetime desc,tid asc)
            """)

        session.execute("""  
            CREATE TABLE tweetsTimelinehash (
                tid bigint,
                tweet_text text,
                datetime TIMESTAMP ,
                quote_count int,
                reply_count int,
                like_count int,
                retweet_count int,
                hashkey text,
                location text,
                type ascii,
                lang ascii,
                keyWords_processed_list list<text>,
                url_list list<text>,
                retweet_source_id bigint,
                mentions list<text>,
                replyto_source_id bigint,
                author text,
                author_screen_name ascii,
                author_id bigint,
                PRIMARY KEY (hashkey,datetime,tid)         
            ) with clustering order by (datetime desc,tid ASC )
            """)
        #
        session.execute("""
                    CREATE TABLE tweetsTimelinekey (
                        tid bigint,
                        tweet_text text,
                        datetime TIMESTAMP ,
                        quote_count int,
                        reply_count int,
                        like_count int,
                        retweet_count int,
                        hashtags list<text>,
                        location text,
                        type ascii,
                        lang ascii,
                        keyWord text,
                        url_list list<text>,
                        retweet_source_id bigint,
                        mentions list<text>,
                        replyto_source_id bigint,
                        author text,
                        author_screen_name ascii,
                        author_id bigint,
                        PRIMARY KEY (keyWord,like_count,tid)
                    ) with clustering order by  (like_count desc, tid asc )
                    """)

        session.execute("""
                            CREATE TABLE tweetsTimelinemention (
                            tid bigint,
                            tweet_text text,
                            datetime TIMESTAMP ,
                            quote_count int,
                            reply_count int,
                            like_count int,
                            retweet_count int,
                            hashtags list<text>,
                            location text,
                            type ascii,
                            lang ascii,
                            keyWords_processed_list list<text>,
                            url_list list<text>,
                            retweet_source_id bigint,
                            mention text,
                            replyto_source_id bigint,
                            author text,
                            author_screen_name ascii,
                            author_id bigint,
                            PRIMARY KEY (mention,datetime,tid)
                            ) with clustering order by  (datetime desc, tid asc )
                            """)

        session.execute("""
                            CREATE TABLE tweetsTimelinedate (
                            tid bigint,
                            tweet_text text,
                            datetime TIMESTAMP ,
                            date ascii,
                            quote_count int,
                            reply_count int,
                            like_count int,
                            retweet_count int,
                            hashtags list<text>,
                            location text,
                            type ascii,
                            lang ascii,
                            keyWords_processed_list list<text>,
                            url_list list<text>,
                            retweet_source_id bigint,
                            mentions list<text>,
                            replyto_source_id bigint,
                            author text,
                            author_screen_name ascii,
                            author_id bigint,
                            PRIMARY KEY (date,like_count,tid)
                            ) with clustering order by  (like_count desc, tid asc )
                            """)

        session.execute("""
                    CREATE TABLE tweetsTimelineloc (
                        tid bigint,
                        tweet_text text,
                        datetime TIMESTAMP ,
                        quote_count int,
                        reply_count int,
                        like_count int,
                        retweet_count int,
                        hashtags list<text>,
                        location text,
                        type ascii,
                        lang ascii,
                        keyWord text,
                        url_list list<text>,
                        retweet_source_id bigint,
                        mentions list<text>,
                        replyto_source_id bigint,
                        author text,
                        author_screen_name ascii,
                        author_id bigint,
                        PRIMARY KEY (location,tid)
                    ) with clustering order by  ( tid asc )
                    """)

        session.execute("""
                            CREATE TABLE tweetsTimelinefreq(
                            date ascii,
                            hashkey text,
                            freq int,
                            PRIMARY KEY (date,freq,hashkey)
                            ) with clustering order by  (freq desc,hashkey ASC )
                            """)

        tweetPrepare = session.prepare('insert into tweetsTimeline JSON ?')
        tweetPreparehash = session.prepare('insert into tweetsTimelinehash JSON ?')
        tweetPreparekey = session.prepare('insert into tweetsTimelinekey JSON ?')
        tweetPreparemention = session.prepare('insert into tweetsTimelinemention JSON ?')
        tweetPreparedate = session.prepare('insert into tweetsTimelinedate JSON ?')
        tweetPrepareLocation = session.prepare('insert into tweetsTimelineloc JSON ?')
        tweetPreparefreq = session.prepare('insert into tweetsTimelinefreq JSON ?')
        print('All done!')
        return tweetPrepare, tweetPreparehash, tweetPreparekey, tweetPreparemention, tweetPreparedate, tweetPreparefreq,tweetPrepareLocation

    def load_users_data(self, p, name, handle, uid, dtime, twid):
        log.info("Inserting into userline keyspace ...")
        # cqlQuery = 'insert into userline("userName","userHandle","userId","dateTime","tweet_id") values (name,handle,uid,dtime,twid)'
        td = datetime.strptime(dtime, "%Y-%m-%d %H:%M:%S")
        session.execute(p, (name, handle, uid, td, twid))

    def load_tweet_data(self, u, twId, body, dtime, qCnt, repCnt, lCnt, rCnt, hash, loc, typ, lang, keywrd, url, rtd,
                        ment, repId):
        log.info("Inserting into tweetsTimeline keyspace ... ")
        td = datetime.strptime(dtime, "%Y-%m-%d %H:%M:%S")
        session.execute(u, twId, body, td, qCnt, repCnt, lCnt, rCnt, hash, loc, typ, lang, keywrd, url, rtd, ment,
                        repId)

    def load_json(self, tw, tweet_dict):
        log.info("Inserting into tweetsTimeline keyspace ... ")
        session.execute(tw, [json.dumps(tweet_dict, indent=4, sort_keys=True, default=str)])

    def create_view(self):
        session.execute('use twissandra');
        session.execute('drop materialized view if exists authortweetQuery');
        session.execute('create materialized view authortweetQuery as select * from tweetsTimeline'
                        ' where author_screen_name is not null and datetime is not null '
                        ' primary key(author_screen_name,datetime) with clustering order by (datetime DESC)')
