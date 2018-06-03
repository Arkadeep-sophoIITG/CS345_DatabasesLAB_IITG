import os
from py2neo import Graph, Node, Relationship, NodeSelector
from datetime import datetime
import json
import time

import logging

PASSWORD = "stud" 
#set your own damn password @$$ol

# log = logging.getLogger()
# log.setLevel('DEBUG')
# handler = logging.StreamHandler()
# handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
# log.addHandler(handler)

graph = Graph("bolt://localhost:7687", password=PASSWORD)
transaction = graph.begin()

path = 'workshop'
filelist = os.listdir(path)
hashmap = {}
hash_counter = {}
num = -1

start = time.time()


def setup_constraints(self):
    try:
        graph.run("CREATE CONSTRAINT ON (user:User) ASSERT user.author_id IS UNIQUE")
        graph.run("CREATE CONSTRAINT ON (tweet:Tweets) ASSERT tweet.tid IS UNIQUE")
        # log.info("Created CONSTRAINTS")
    except:
        pass
    return


# source : stackoverflow : https://stackoverflow.com/questions/27784313/py2neo-graph-cypher-execute

def create_node(label, properties):
    query = "CREATE (:{}".format(label) + " {properties})"
    params = dict(properties=properties)
    graph.run(query, params)
    # print("Done")


def define_relationship_user2tweet(dict1, dict2, rel_label):
    query = 'MATCH (user:Users {}), (tweet:Tweets{}) CREATE (user)-[post:{}]->(tweet) RETURN post'.format(dict1, dict2,
                                                                                                          rel_label)
    # print(query)
    graph.run(query)
    # print("Done")


def define_relationship_tweet2hashtag(dict1, dict2, rel_label):
    query = 'MATCH (tweet:Tweets {}), (hash:HashTag{}) CREATE (tweet)-[contain:{}]->(hash) RETURN contain'.format(dict1,
                                                                                                                  dict2,
                                                                                                                  rel_label)
    # print(query)
    graph.run(query)
    # print("Done")


def define_relationship_tweet2mention(dict1, dict2, rel_label):
    query = 'MATCH (t1:Tweets {}), (user:Users {}) CREATE (t1)-[retw:{}]->(user) RETURN retw'.format(dict1, dict2,
                                                                                                     rel_label)
    # print(query)
    graph.run(query)
    # print("Done")


def define_relationship_tweet2retweet(dict1, dict2, rel_label):
    query = 'MATCH (t1:Tweets {}), (t2:Tweets {}) CREATE (t1)-[retw:{}]->(t2) RETURN retw'.format(dict1, dict2,
                                                                                                  rel_label)
    # print(query)
    graph.run(query)
    # print("Done")


def define_relationship_tweet2replytweet(dict1, dict2, rel_label):
    query = 'MATCH (t1:Tweets {}), (t2:Tweets {}) CREATE (t1)-[reply:{}]->(t2) RETURN reply'.format(dict1, dict2,
                                                                                                    rel_label)
    # print(query)
    graph.run(query)
    # print("Done")


def create_index():
    graph.run("CREATE INDEX ON  :Users(author_screen_name)")
    graph.run("CREATE INDEX ON :Tweets(tid)")
    graph.run("CREATE INDEX ON :HashTag(hashtag)")


create_index()
check_dict = {}
tweet_check_dict = {}
hash_dict = {}
mentions_dict = {}
retweet_dict = {}
reply_dict = {}
for i in filelist:
    with open(path + "/" + str(i)) as data_file:
        data = json.load(data_file)
        # print("Opening a new file")
        for k, v in data.items():
            td = datetime.strptime(v['datetime'], "%Y-%m-%d %H:%M:%S")
            str(td).strip('.')
            check_dict[v['author_screen_name']] = check_dict.get(v['author_screen_name'], 0) + 1
            tweet_check_dict[v['tid']] = tweet_check_dict.get(v['tid'], 0) + 1
            user_dict = {'author_screen_name': v['author_screen_name'], 'author_id': int(v['author_id']),
                         'author': v['author']}
            # #print(user_dict)
            tweet_dict = {'tid': v['tid'], 'datetime': v['datetime'], 'tweet_text': v['tweet_text']
                , 'location': v['location'], 'type': v['type']}
            # print(tweet_dict)
            hash_cnt = {}

            try:
                if check_dict[v['author_screen_name']] == 1:
                    create_node("Users", user_dict)
                else:
                    pass
                    # print("User already exists")
                if tweet_check_dict[v['tid']] == 1:
                    # print("Creating Tweet")
                    create_node("Tweets", tweet_dict)
                    # print("Done creating tweet")
            except:
                pass
                # log.error("Couldnot create node users/tweet")

            if v['hashtags']:
                for e in v['hashtags']:
                    hash_dict[e] = hash_dict.get(e, 0) + 1
                    if hash_dict[e] == 1:
                        hash_cnt = {'tid': v['tid'], 'hashtag': e}
                        try:
                            create_node("HashTag", hash_cnt)
                        except:
                            pass
                            # log.error("Couldnot create node hashtag")

# print("Done creating Node")


for i in filelist:
    with open(path + "/" + str(i)) as data_file:
        data = json.load(data_file)
        # print("Opening a new file")
        for k, v in data.items():
            user = "{author_screen_name: " + '"' + v['author_screen_name'] + '"' + "}"
            tweet = "{tid: " + '"' + v['tid'] + '"' + "}"
            define_relationship_user2tweet(user, tweet, "POSTS")
            if v['mentions']:
                for m in v['mentions']:
                    mentions_dict[m] = mentions_dict.get(m, 0) + 1
                    if mentions_dict[m] == 1 and m not in check_dict:
                        mentions_cnt = {'author_screen_name': m, 'tid': v['tid']}
                        try:
                            create_node("Users", mentions_cnt)
                        except:
                            pass
                            # log.error("Already made user node")
                    t1 = "{tid: " + '"' + v['tid'] + '"' + "}"
                    h1 = "{author_screen_name: " + '"' + m + '"' + "}"
                    define_relationship_tweet2mention(t1, h1, "MENTIONS")

            if v['type'] == 'retweet' and v['retweet_source_id']:
                retweet_dict[v['retweet_source_id']] = retweet_dict.get(v['retweet_source_id'], 0) + 1
                if retweet_dict[v['retweet_source_id']] == 1 and v['retweet_source_id'] not in tweet_check_dict:
                    retweet_cnt = {'tid': v['retweet_source_id'], 'retweeted': v['tid']}
                    try:
                        create_node("Tweets", retweet_cnt)
                    except:
                        pass
                        # log.error("Already made tweets node")
                t1 = "{tid: " + '"' + v['tid'] + '"' + "}"
                t2 = "{tid: " + '"' + v['retweet_source_id'] + '"' + "}"
                define_relationship_tweet2retweet(t1, t2, "RETWEETOF")

            if v['type'] == 'Reply' and v['replyto_source_id']:
                reply_dict[v['replyto_source_id']] = reply_dict.get(v['replyto_source_id'], 0) + 1
                if reply_dict[v['replyto_source_id']] == 1 and v['replyto_source_id'] not in tweet_check_dict:
                    reply_cnt = {'tid': v['replyto_source_id'], 'replied': v['tid']}
                    try:
                        create_node("Tweets", reply_cnt)
                    except:
                        pass
                        # log.error("Already made tweets node")

                t1 = "{tid: " + '"' + v['tid'] + '"' + "}"
                t2 = "{tid: " + '"' + v['replyto_source_id'] + '"' + "}"
                define_relationship_tweet2replytweet(t1, t2, "REPLYOF")

            if v['hashtags']:
                for e in v['hashtags']:
                    t1 = "{tid: " + '"' + v['tid'] + '"' + "}"
                    h1 = "{hashtag: " + '"' + e + '"' + "}"
                    define_relationship_tweet2hashtag(t1, h1, "HASHTAG")

end = time.time() - start
print(end)
