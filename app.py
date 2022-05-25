from logging import NullHandler
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return '<Blog %r>' % self.id
    


@app.route('/')
def index():
    blogs = Blog.query.all();

    return render_template('index.html', blogs=blogs)


@app.route('/blog/<int:id>')
def blog_details(id):
    blog = Blog.query.get_or_404(id)
    return render_template('blog_details.html', blog=blog)

@app.route('/new-blog', methods=['GET', 'POST'])
def new_blog():
    if request.method == 'POST':
        title = request.form["title"]
        body = request.form["body"]
        author = request.form["author"]

        new_blog = Blog(title=title, body=body, author=author)

        try:
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem adding your blog'
    else:
        return render_template('new_blog.html')

@app.route('/delete/<int:id>')
def delete_blog(id):
    blog = Blog.query.get_or_404(id)
    try:
        db.session.delete(blog)
        db.session.commit()
        return redirect('/')
    
    except:
        return 'There was problem deleting the blog'




if __name__ == "__main__":
    app.run(debug=True)