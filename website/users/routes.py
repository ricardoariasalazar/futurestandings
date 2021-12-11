from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from website import db, bcrypt
from website.database import User, Post
from website.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from website.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

# User registration page
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
      return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # Hash the password given 
      user = User(username=form.username.data, email=form.email.data, password=hashed_password) # Create the user in db
      db.session.add(user)
      db.session.commit()
      flash(f'{form.username.data} your account has been created!', 'success')
      return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


# User login page
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
      return redirect(url_for('main.home'))
    form = LoginForm() # Get the data input 
    if form.validate_on_submit():
      user = User.query.filter_by(email=form.email.data).first() # Find if the user exists in the database
      if user and bcrypt.check_password_hash(user.password, form.password.data): # Check if exists and the password 
        login_user(user, remember=form.remember.data) # Go to an user space
        next_page = request.args.get('next') # If I required to access a page that only users can get access to, get the parameter
        return redirect(next_page) if next_page else redirect(url_for('main.home')) # If next exist redirect them after logging in
      else:
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# Logout button redirected to home page
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# Account profile page with login requirement
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()
  if form.validate_on_submit():
    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Your account has been updated', 'success')
    return redirect(url_for('users.account'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email

  image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
  return render_template('account.html', title='Account', image_file=image_file, form=form)


# User Page
@users.route("/user/<string:username>")
def user_post(username):
    page = request.args.get('page', 1, type=int) # Get the arguments of the page number
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) 
    # Instead of do a query of all we do it by pages, 5 per page in desc order
    return render_template('user_post.html', posts=posts, user=user) # Render template getting the posts from the database


# Account profile page with login requirement
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
  if current_user.is_authenticated: # Be sure they are logged out
      return redirect(url_for('main.home'))
  form=RequestResetForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    send_reset_email(user)
    flash('Email has been sent with instruction to reset your password.', 'info')
    return redirect(url_for('users.login'))
  return render_template('reset_request.html', title='Reset Password', form=form)

# Account profile page with login requirement
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
  if current_user.is_authenticated: # Be sure they are logged out
      return redirect(url_for('main.home'))
  user = User.verify_reset_token(token)
  if user is None:
    flash('That is an invalid token', 'warning')
    return redirect(url_for('reset_request'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # Hash the password given 
      user.password = hashed_password
      db.session.commit()
      flash('Your password has been updated!', 'success')
      return redirect(url_for('users.login'))
  return render_template('reset_token.html', title='Reset Password', form=form)

