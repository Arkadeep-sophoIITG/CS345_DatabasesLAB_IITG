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
session.set_keyspace("assignment")


def preparestatements(session):
    session.set_keyspace('assignment')
    authorCluster = session.prepare(
        'select date,freq,author_id from tweetsactiveid where "date" = ?')
    session.set_keyspace('assignment2')
    hashCLuster = session.prepare(
        'select date,freq,hashkey,mention from tweetsmentionhash where "date" = ?')
    return authorCluster, hashCLuster


def query2(session, authorCluster, name):
    session.set_keyspace('assignment2')
    outtable = "<table class='table table-hover'><thead>"
    header = ['date', 'hashtag', 'mention', 'frequency']
    for jj in header:
        outtable += "<th>" + str(jj) + "</th>"
    outtable += "</thead><tbody>"
    raw_output = session.execute(authorCluster, (name,))
    for row in raw_output:
        outtable += "<tr>"
        li = [row.date, row.hashkey, row.mention, row.freq]
        for bla in li:
            outtable += "<td>" + str(bla) + "</td>"
        outtable += "</tr>"
    outtable += "</tbody></table>"
    return outtable


def query1(session, authorCluster, name):
    session.set_keyspace('assignment')
    outtable = "<table class='table table-hover'><thead>"
    header = ['Date', 'Author_id', 'Frequency']
    for jj in header:
        outtable += "<th>" + str(jj) + "</th>"
    outtable += "</thead><tbody>"
    print(outtable)
    raw_output = session.execute(authorCluster, (name,))
    for row in raw_output:
        print(">>>", row)
        print(outtable)
        outtable += "<tr>"
        li = [row.date, row.author_id, row.freq]
        for bla in li:
            outtable += "<td>" + str(bla).replace('\n', ' ').replace('\'', '\\\'').replace('\"', '\\\"').replace('\t',
                                                                                                                 ' ').replace(
                '\r', ' ') + "</td>"
        outtable += "</tr>"
    outtable += "</tbody></table>"
    print(outtable)
    return outtable


@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.method)
    output = None
    if request.method == 'POST':
        name = request.form['name']
        index = request.form['index']
        print(name, index)
        authc, hashc = preparestatements(session)
        if index == "1":
            output = query1(session, authc, name)
        if index == "2":
            output = query2(session, hashc, name)

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
