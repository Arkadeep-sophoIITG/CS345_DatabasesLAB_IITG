from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from cassandra.cluster import Cluster
from datetime import datetime
import json
import logging
import query7

log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'b\'N\x1cW\xe4%p\xee\xf1\xd6\xc2\xc5;\x1au\xb5\x7f]$+\x88\x90\xa5\x84O\x0b\''

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()
session.set_keyspace("twissandra")


def preparestatements(session):
    authorCluster = session.prepare(
        'select tid,tweet_text,datetime,author_id,author,author_screen_name,location,lang from tweetsTimeline where "author_screen_name" = ?')
    hashCLuster = session.prepare(
        'select tid,hashkey,tweet_text,datetime,author_id,author,author_screen_name,location,lang from tweetsTimelinehash where "hashkey" = ?')
    keywordCluster = session.prepare(
        'select tid,keyword,tweet_text,datetime,author_id,author,author_screen_name,location,lang from tweetsTimelinekey where "keyword" = ?')

    mentionCLuster = session.prepare(
        'select tid,mention,tweet_text,datetime,author_id,author,author_screen_name,location,lang from tweetsTimelinemention where "mention" = ?')

    dateCluster = session.prepare(
        'select tid,like_count,tweet_text,datetime,author_id,author,author_screen_name,location,lang from tweetsTimelinedate where "date" = ?')

    locCluster = session.prepare(
        'select tid,like_count,tweet_text,datetime,author_id,author,author_screen_name,location,lang from tweetsTimelineloc where "location" = ?')

    deleteC = session.prepare('delete from tweetsTimelinedate where date = ?')
    return authorCluster, hashCLuster, keywordCluster, mentionCLuster, dateCluster, locCluster, deleteC


def query1(session, authorCluster, name):
    outtable = "<table class='table table-hover'><thead>"
    header = ['Tweet id', 'Text', 'datetime', 'author id', 'user handle', 'location', 'language']
    for jj in header:
        outtable += "<th>" + str(jj) + "</th>"
    outtable += "</thead><tbody>"
    raw_output = session.execute(authorCluster, (name,))
    for row in raw_output:
        outtable += "<tr>"
        li = [row.tid, row.tweet_text, row.datetime, row.author_id, row.author_screen_name, row.location, row.lang]
        for bla in li:
            outtable += "<td>" + str(bla) + "</td>"
        outtable += "</tr>"
    outtable += "</tbody></table>"
    return outtable


def query2(session, authorCluster, name):
    outtable = "<table class='table table-hover'><thead>"
    header = ['Tweet id', 'HashTag', 'Text', 'datetime', 'author id', 'user handle', 'location', 'language']
    for jj in header:
        outtable += "<th>" + str(jj) + "</th>"
    outtable += "</thead><tbody>"
    print(outtable)
    raw_output = session.execute(authorCluster, (name,))
    for row in raw_output:
        print(">>>", row)
        print(outtable)
        outtable += "<tr>"
        li = [row.tid, row.hashkey, row.tweet_text, row.datetime, row.author_id, row.author_screen_name, row.location,
              row.lang]
        for bla in li:
            outtable += "<td>" + str(bla).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',
                                                                                                                 ' ').replace(
                '\r', ' ') + "</td>"
        outtable += "</tr>"
    outtable += "</tbody></table>"
    print(outtable)
    return outtable


def query3(session, authorCluster, name):
    outtable = "<table class='table table-hover'><thead>"
    header = ['Tweet id', 'Keyword', 'Text', 'datetime', 'author id', 'user handle', 'location', 'language']
    for jj in header:
        outtable += "<th>" + str(jj) + "</th>"
    outtable += "</thead><tbody>"
    print(outtable)
    raw_output = session.execute(authorCluster, (name,))
    for row in raw_output:
        print(">>>", row)
        print(outtable)
        outtable += "<tr>"
        li = [row.tid, row.keyword, row.tweet_text, row.datetime, row.author_id, row.author_screen_name, row.location,
              row.lang]
        for bla in li:
            outtable += "<td>" + str(bla).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',
                                                                                                                 ' ').replace(
                '\r', ' ') + "</td>"
        outtable += "</tr>"
    outtable += "</tbody></table>"
    print(outtable)
    return outtable


def query4(session, authorCluster, name):
    outtable = "<table class='table table-hover'><thead>"
    header = ['Tweet id', 'Mention', 'Text', 'datetime', 'author id', 'user handle', 'location', 'language']
    for jj in header:
        outtable += "<th>" + str(jj) + "</th>"
    outtable += "</thead><tbody>"
    print(outtable)
    raw_output = session.execute(authorCluster, (name,))
    for row in raw_output:
        print(">>>", row)
        print(outtable)
        outtable += "<tr>"
        li = [row.tid, row.mention, row.tweet_text, row.datetime, row.author_id, row.author_screen_name, row.location,
              row.lang]
        for bla in li:
            outtable += "<td>" + str(bla).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',
                                                                                                                 ' ').replace(
                '\r', ' ') + "</td>"
        outtable += "</tr>"
    outtable += "</tbody></table>"
    return outtable


def query5(session, authorCluster, name):
    outtable = "<table class='table table-hover'><thead>"
    header = ['Tweet id', 'Likes', 'Text', 'datetime', 'author id', 'user handle', 'location', 'language']
    for jj in header:
        outtable += "<th>" + str(jj) + "</th>"
    outtable += "</thead><tbody>"
    print(outtable)
    raw_output = session.execute(authorCluster, (name,))
    for row in raw_output:
        print(">>>", row)
        print(outtable)
        outtable += "<tr>"
        li = [row.tid, row.like_count, row.tweet_text, row.datetime, row.author_id, row.author_screen_name,
              row.location, row.lang]
        for bla in li:
            outtable += "<td>" + str(bla).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',
                                                                                                                 ' ').replace(
                '\r', ' ') + "</td>"
        outtable += "</tr>"
    outtable += "</tbody></table>"
    return outtable


def query6(session, authorCluster, name):
    outtable = "<table class='table table-hover'><thead>"
    header = ['Tweet id', 'Likes', 'Text', 'datetime', 'author id', 'user handle', 'location', 'language']
    for jj in header:
        outtable += "<th>" + str(jj) + "</th>"
    outtable += "</thead><tbody>"
    print(outtable)
    raw_output = session.execute(authorCluster, (name,))
    for row in raw_output:
        print(">>>", row)
        print(outtable)
        outtable += "<tr>"
        li = [row.tid, row.like_count, row.tweet_text, row.datetime, row.author_id, row.author_screen_name,
              row.location, row.lang]
        for bla in li:
            outtable += "<td>" + str(bla).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',
                                                                                                                 ' ').replace(
                '\r', ' ') + "</td>"
        outtable += "</tr>"
    outtable += "</tbody></table>"
    return outtable


def querybig(session, name):
    outtable = "<table class='table table-hover'><thead>"
    header = ['HashTag']
    for jj in header:
        outtable += "<th>" + str(jj) + "</th>"
    outtable += "</thead><tbody>"
    print(outtable)
    lists = query7.query_output(name)
    # print(">>>", row)
    print(outtable)
    outtable += "<tr>"
    for bla in lists:
        outtable += "<td>" + str(bla).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',
                                                                                                             ' ').replace(
            '\r', ' ') + "</td>"
    outtable += "</tr>"
    outtable += "</tbody></table>"
    return outtable


@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.method)
    output = None
    if request.method == 'POST':
        name = request.form['name']
        index = request.form['index']
        print(name, index)
        authc, hashc, keyC, menC, dateC, locC, delC = preparestatements(session)
        if index == "1":
            output = query1(session, authc, name)
        if index == "2":
            output = query2(session, hashc, name)
        if index == "3":
            output = query3(session, keyC, name)
        if index == "4":
            output = query4(session, menC, name)
        if index == "5":
            output = query5(session, dateC, name)
        if index == "6":
            output = query6(session, locC, name)
        if index == "7":
            output = querybig(session, name)
        if index == "8":
            session.execute(delC, (name,))
    return render_template('query.html', output=output)


# @app.route("/", methods=['GET', 'POST'])
# def hello():
#     form = ReusableForm(request.form)
#     if request.method == 'POST':
#         name = request.form['name']
#         print(name)
#         prepare = query7.preparestatements()
#         output = query7.query(prepare, str(name))
#
#     return render_template('hello.html', form=form)
# #

if __name__ == '__main__':
    app.run(debug=True)
