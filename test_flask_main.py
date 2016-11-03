from flask_main import *
import arrow

#CONDITION
#Mongod must be running on port 27333 for nosetest to function
#Must have at least 5 memos in the database

def test_create():
  """
  Test creation of memos
  """

  memo = "this is my memo"
  date = "2016-11-01"
  assert(create_helper(memo, date)["text"] == memo)
  assert(create_helper(memo, date)["date"] == arrow.get(date).replace(tzinfo = tz.tzlocal()).isoformat())

  memo = "this is another memo"
  date = "2016-02-28"
  assert(create_helper(memo, date)["text"] == memo)
  assert(create_helper(memo, date)["date"] == arrow.get(date).replace(tzinfo = tz.tzlocal()).isoformat())
  
  #empty memo
  memo = ""
  date = "2016-01-01"
  assert(create_helper(memo, date)["text"] == memo)
  assert(create_helper(memo, date)["date"] == arrow.get(date).replace(tzinfo = tz.tzlocal()).isoformat())

  return None

def test_destroy():
  """
  test removal of memos
  This tests that the correct memo to be removed is found.
  """
  sorted_memos = sort_memos(get_memos())  

  to_destroy_str = "1,"
  to_destroy = to_destroy_str.strip(',').split(',')
  destroyed = []
  for index in to_destroy:
    destroyed.append(sorted_memos[int(index)-1])
  assert(destroy_helper(to_destroy_str) ==  destroyed)

  #if butto clicked but no boxes checked
  to_destroy_str = ""
  destroyed = []
  assert(destroy_helper(to_destroy_str) ==  destroyed)

  to_destroy_str = "1,5,"
  to_destroy = to_destroy_str.strip(',').split(',')
  destroyed = []
  for index in to_destroy:
    destroyed.append(sorted_memos[int(index)-1]) 
  assert(destroy_helper(to_destroy_str) ==  destroyed)

  return None


def test_humanize():
  """
  test humanization of dates
  """
  now = arrow.now()

  date = now.replace(days =- 2) 
  assert(humanize_arrow_date(date) == "2 days ago" )

  date = now.replace(days =- 1)
  assert(humanize_arrow_date(date) == "Yesterday" )

  date = now.replace(days =- 0)
  assert(humanize_arrow_date(date) == "Today" )
  
  date = now.replace(days =+ 1)
  assert(humanize_arrow_date(date) == "Tomorrow" )

  return None

