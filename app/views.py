from flask import render_template, abort
from app import app
try:
    import pymongo
    db = pymongo.MongoClient().get_database('codyjhanson')
    posts = db.get_collection("posts")
    projects = db.get_collection("projects")
except:
    app.logger.info("Unable to connect to posts database")

def preview_text(text):
    #TODO
    return "Test test test test test"

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/blog')
@app.route('/blog.html')
def blog():
    blogposts = []
    try:
        cursor = posts.find({})
        for post in cursor:
            post_dict = {}
            post_dict['uid'] = post['uid']
            post_dict['preview_text'] = preview_text(post['content'])
            post_dict['title'] = post['title']
            blogposts.append(post_dict)
    except:
        pass
    return render_template('blog.html', posts=blogposts)

@app.route('/projects')
@app.route('/projects.html')
def projects():
    return render_template('projects.html')

@app.route('/contact')
@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/blog/<post>')
def blogpost(post=None):
    document = posts.find_one({'uid' : post})
    return render_template('post.html', title=document['title'],
                           date=document['date'],content=document['content'])
@app.route('/projects/project')
def project(project=None):
    document = projects.find_one({'uid' : project})
    return render_template('post.html', title=document['title'],
                           date=document['date'],content=document['content'])

