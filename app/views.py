from flask import render_template, abort
from app import app
import pymongo
db = pymongo.MongoClient().get_database('codyjhanson')
posts = db.get_collection("posts")

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/blog')
@app.route('/blog.html')
def blog():
    return render_template('blog.html')

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

