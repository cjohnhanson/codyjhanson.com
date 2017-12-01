#!/usr/bin/python
"""Manage posts
Usage:
  manage_posts.py publish FILE --uid UID --title TITLE [-p]
  manage_posts.py unpublish --uid UID
  
Options:
  -h --help    Display this message
  -p --prod    Publish/unpublish to production instance (default is to local dev instance)
"""
import datetime, pymongo as pm
from docopt import docopt

def classy_date(date):
    """Make a datetime look classy"""
    return "{} {}, {}".format(date.day, date.strftime("%B"), date.year)

def publish(infile, title, uid, collection):
    """Publish post from file to either dev or prod"""
    with open(infile, 'r') as content_file:
        post = {}
        post['title'] = title
        post['uid'] = uid
        post['date'] = classy_date(datetime.datetime.today())
        post['content'] = content_file.read()
        content_file.close()
        return collection.insert_one(post)


def unpublish(uid, collection):
    """Unpublish post with given uid from either dev or prod"""
    return collection.delete_one({'uid' : uid})

def main():
    args = docopt(__doc__)
    env = 'prod' if args['--prod'] else 'dev'
    if env == 'prod':
         collection = pm.MongoClient('mongodb://codyjhanson.com:27017').get_database("codyjhanson").get_collection("posts")
    else:
         collection = pm.MongoClient().get_database("codyjhanson").get_collection("posts")
    if args['publish']:
        publish(args['FILE'], args['UID'], args['TITLE'], collection)
    elif args['unpublish']:
        unpublish(args['UID'], collection)
    return 0

if __name__ == '__main__':
    main()
