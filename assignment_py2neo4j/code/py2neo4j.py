from flask import Flask, render_template, request

app = Flask(__name__)

import os
from py2neo import Graph, Node, Relationship, NodeSelector
from datetime import datetime
import json

import logging

PASSWORD = "stud"

# log = logging.getLogger()
# log.setLevel('DEBUG')
# handler = logging.StreamHandler()
# handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
# log.addHandler(handler)

graph = Graph("bolt://localhost:7687", password=PASSWORD)
transaction = graph.begin()


def query1(author_screen_name):
    h1 = "{hashtag: " + '"' + author_screen_name + '"' + "}"
    query1 = " match (h:HashTag{})<-[:HASHTAG]-(t:Tweets)<-[:POSTS]-(u:Users)return u,h,collect(t.tid),count(*)  order by count(*) desc limit 3".format(
        h1)
    w = graph.run(query1)
    outtable = "<table class='table table-hover'><thead>"
    header = ['User', 'Hashtag', 'Tids', 'Tweet_count']
    outtable += "</thead><tbody>"
    for jj in header:
        outtable += "<th>" + str(jj) + "</th>"
    for e in w:
        outtable += "<tr>"
        print(e)
        li = [e['u']['author_screen_name'], e['h']['hashtag'], e['collect(t.tid)'], e['count(*)']]
        for bla in li:
            outtable += "<td>" + str(bla) + "</td>"
        outtable += "</tr>"
    outtable += "</tbody></table>"
    return outtable


def query2(author_screen_name):
    author_screen_name = '"' + author_screen_name + '"'
    query1 = "match (u1:Users)<-[:MENTIONS]-(t:Tweets)-[:MENTIONS]->(u2:Users) where t.location={} and u1.author_screen_name > u2.author_screen_name and t.type='Tweet' return u1.author_screen_name as uu,u2.author_screen_name as uu2,collect(t),count(t) order by count(t) desc limit 3".format(
        author_screen_name)
    w = graph.run(query1)
    outtable = "<table class='table table-hover'><thead>"
    header = ['Location', 'Usermention1', 'Usermention2', 'Tids', 'Co-occurence_Count']
    outtable += "</thead><tbody>"
    for jj in header:
        outtable += "<th>" + str(jj) + "</th>"
    for tweets in w:
        print(tweets)
        outtable += "<tr>"
        li = [tweets['collect(t)'], tweets['uu'], tweets['uu2'],
              tweets['collect(t)'], tweets['count(t)']]
        for bla in li:
            outtable += "<td>" + str(bla) + "</td>"
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
        if index == "1":
            output = query1(name)
        if index == "2":
            output = query2(name)

    return render_template('query.html', output=output)


if __name__ == '__main__':
    app.run(debug=True)
