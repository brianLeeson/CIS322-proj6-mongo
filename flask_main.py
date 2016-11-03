"""
Flask web app connects to Mongo database.
Keep a simple list of dated memoranda.

Representation conventions for dates: 
   - We use Arrow objects when we want to manipulate dates, but for all
     storage in database, in session or g objects, or anything else that
     needs a text representation, we use ISO date strings.  These sort in the
     order as arrow date objects, and they are easy to convert to and from
     arrow date objects.  (For display on screen, we use the 'humanize' filter
     below.) A time zone offset will 
   - User input/output is in local (to the server) time.  
"""


import random

import flask
from flask import g
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify

import json
import logging

import pymongo
import sys

import secrets.admin_secrets
import secrets.client_secrets

# Date handling 
import arrow    # Replacement for datetime, based on moment.js
# import datetime # But we may still need time
from dateutil import tz  # For interpreting local times

# Mongo database
from pymongo import MongoClient
import secrets.admin_secrets
import secrets.client_secrets
MONGO_CLIENT_URL = "mongodb://{}:{}@localhost:{}/{}".format(
    secrets.client_secrets.db_user,
    secrets.client_secrets.db_user_pw,
    secrets.admin_secrets.port, 
    secrets.client_secrets.db)

###
# Globals
###
import CONFIG
app = flask.Flask(__name__)
app.secret_key = CONFIG.secret_key

####
# Database connection per server process
###

try: 
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, secrets.client_secrets.db)
    collection = db.dated

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)


###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
  app.logger.debug("Main page entry")
  g.memos = sort_memos(get_memos())
  return flask.render_template('index.html')

@app.route("/new")
def new():
  app.logger.debug("Memo entry page")
  return flask.render_template('new.html')

@app.route("/create")
def create():
  """
  This creates the memo in the db
  """
  app.logger.debug("Entering Create")
  
  memo = request.args.get("memo", type=str)
  date = request.args.get("date", type=str)
  
  collection.insert(create_helper(memo, date))
  
  rslt = { "key" : "test" }
  return jsonify(result = rslt)

def create_helper(memo, date):
  """
  takes two strings, 
    memo:text of memo
    date:date of memo
  adds the memo to the db  

  returns a dict representing the memo
  """
  
  #handle timezones
  date = arrow.get(date)
  date = date.replace(tzinfo=tz.tzlocal())

  record = { "UID": str(random.random()), 
             "type": "dated_memo", 
             "date": date.isoformat(),
             "text": memo
            }
  return record

@app.route("/destroy")
def destroy():
  """
  This creates the memo in the db
  """
  app.logger.debug("Entering Destroy")
  
  checked = request.args.get("checked", type=str)
  to_remove =  destroy_helper(checked)
  
  for memo in to_remove:
    collection.remove({'UID': memo["UID"]})

  rslt = { "key" : "test" }
  return jsonify(result = rslt)

def destroy_helper(checked):
  """
  takes string of numbers sep by commas
  removes those items from the database
  returns a list of memos that were destroyed
  """
  #print("Checked:", checked)
  checkedIndex = (checked.split(','))
  sorted_memos = sort_memos(get_memos())
  
  to_remove = []
  for index in range(len(checkedIndex)-1):
    i = int(checkedIndex[index])-1
    memo = sorted_memos[i]
    to_remove.append(memo)

  #print("to_remove:", to_remove) 
  return to_remove
  
@app.errorhandler(404)
def page_not_found(error):
  app.logger.debug("Page not found")
  return flask.render_template('page_not_found.html',
                                 badurl=request.base_url,
                                 linkback=url_for("index")), 404

#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'humanize' )
def humanize_arrow_date( date ):
    """
    Date iuis internal UTC ISO format string.
    Output should be "today", "yesterday", "in 5 days", etc.
    Arrow will try to humanize down to the minute, so we
    need to catch 'today' as a special case. 
    """
    
    print("date is:", date)
    #close dates should be related by days, not hours.
    try:
        then = arrow.get(date).to('local')
        now = arrow.utcnow().to('local')
        yesterday = now.replace(days =- 1)
        tomorrow  = now.replace(days =+ 1)
        if then.date() == now.date():
            human = "Today"
        elif (then.date() == yesterday.date()):
            human = "Yesterday"
        elif (then.date() == tomorrow.date()):
            human = "Tomorrow"
        else: 
            human = then.humanize(now)
    except: 
        human = date
    print("return is:", human)
    return human

#############
#
# Functions available to the page code above
#
##############
def get_memos():
    """
    Returns all memos in the database, in a form that
    can be inserted directly in the 'session' object.
    """
    records = [ ]
    for record in collection.find( { "type": "dated_memo" } ):
        record['date'] = arrow.get(record['date']).isoformat()
        del record['_id']
        records.append(record)
    return records 

def sort_memos(records):
  records = sorted(records, key=lambda rec: rec['date'])
  return records

if __name__ == "__main__":
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT,host="0.0.0.0")

    
