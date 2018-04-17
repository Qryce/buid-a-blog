from flask import Flask, request, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:1234@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True #output in terminal 
db = SQLAlchemy(app) #create db object
 
class Blog(db.Model):     #create Blog class 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body, pub_date=None): #constructor
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

@app.route("/", methods=[ "GET"])
def index():

    return render_template('blog.html', title="Build A Blog!!!!!") 
    
@app.route("/blog", methods=["GET"])   
def blog():

    blogs = Blog.query.all()
    return render_template('blog.html', title="Build A Blog", blogs=blogs)

@app.route("/blogpost", methods=["GET"])
def blogpost():

    blog_id = request.args.get('id')
    blog = Blog.query.filter_by(id=blog_id).first()
    return render_template('blogpost.html', blog=blog)

@app.route("/newpost", methods=["POST", "GET"])    
def newpost():

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        body = request.form['body']
        new_blog = Blog(blog_title, body)
        db.session.add(new_blog)
        db.session.commit()
        id = new_blog.id
        return redirect(url_for("blogpost", id=id)) #pass primitive type
    else:
        return render_template("/newpost.html")
    
if __name__ == '__main__':
    app.run()