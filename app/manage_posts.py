#!/usr/bin/python
"""Manage posts
Usage:
  manage_posts.py setup 
  manage_posts.py list [--project]
  manage_posts.py publish FILE --uid UID --title TITLE [--project]
  manage_posts.py unpublish --uid UID
  
Options:
  -h --help    Display this message
  --project    Operate on the projects collection instead of posts
"""
import base64, datetime, getpass, markdown2, pymongo as pm
from docopt import docopt
    
def setup_db(name):
    """Setup the database with posts/projects collections, and user.
    Stores the password encoded in pwd.txt file
    """
    #TODO

def classy_date(date):
    """Make a datetime look classy"""
    return "{} {}, {}".format(date.day, date.strftime("%B"), date.year)

def publish(infile, uid, title, collection):
    """Publish post from file to either dev or prod"""
    with open(infile, 'r') as content_file:
        post = {}
        post['title'] = title
        post['uid'] = uid
        post['date'] = classy_date(datetime.datetime.today())
        post['content'] = markdown2.markdown(content_file.read(), extras=["fenced-code-blocks"])
        content_file.close()
        return collection.insert_one(post)


def unpublish(uid, collection):
    """Unpublish post with given uid from either dev or prod"""
    return collection.delete_one({'uid' : uid})

def list_posts(collection):
    """List all posts currently in the database"""
    for post in collection.find():
        print post['title']
    
def main():
    args = docopt(__doc__)
    db = pm.MongoClient().get_database("codyjhanson")
    if args["setup"]:
        return setup()
    with open("pwd.txt") as pwdfile:
        db.authenticate("cody", pwdfile.read().strip())
        pwdfile.close()
    collection = db.get_collection("projects" if args["--project"] else "posts")
    if args['publish']:
        publish(args['FILE'], args['UID'], args['TITLE'], collection)
    elif args['unpublish']:
        unpublish(args['UID'], collection)
    elif args['list']:
        list_posts(collection)
    return 0

if __name__ == '__main__':
    main()
