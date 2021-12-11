from flask import Blueprint, render_template, request
from website.database import Post

main = Blueprint('main', __name__)

# Home Page
@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int) # Get the arguments of the page number
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) 
    # Instead of do a query of all we do it by pages, 5 per page in desc order
    return render_template('home.html', posts=posts) # Render template getting the posts from the database

# About Page
@main.route("/about")
def about():
    return render_template('about.html', title='About')