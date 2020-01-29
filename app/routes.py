from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
from app import app, db
from app.forms import EditProfileForm, LoginForm, PredictionForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm
from app.email import send_password_reset_email
from app.models import User, Prediction
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    if not current_user.is_anonymous:
        page = request.args.get('page', 1, type=int)
        predictions = current_user.followed_predictions().paginate(
            page, app.config['PREDICTIONS_PER_PAGE_INDEX'], False)
        next_url = url_for('index', page=predictions.next_num) if predictions.has_next else None
        prev_url = url_for('index', page=predictions.prev_num) if predictions.has_prev else None
        return render_template('index.html', title='Home', predictions=predictions.items,
                                next_url=next_url, prev_url=prev_url)
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now my friend!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    predictions = user.prediction_ids.order_by(Prediction.timestamp.desc()).paginate(
        page, app.config['PREDICTIONS_PER_PAGE_USER'], False)
    next_url = url_for('user', username=user.username, page=predictions.next_num) \
        if predictions.has_next else None
    prev_url = url_for('user', username=user.username, page=predictions.prev_num) \
        if predictions.has_prev else None
    return render_template('user.html', user=user, predictions=predictions.items,
                           next_url=next_url, prev_url=prev_url)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot (un)follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    if not current_user.is_anonymous:
        form = PredictionForm()
        if form.validate_on_submit():
            prediction = Prediction(body=form.prediction.data, author=current_user)
            db.session.add(prediction)
            db.session.commit()
            flash('Your prediction is now posted!')
            return redirect(url_for('explore'))
        page = request.args.get('page', 1, type=int)
        predictions = Prediction.query.order_by(Prediction.timestamp.desc()).paginate(
            page, app.config['PREDICTIONS_PER_PAGE_INDEX'], False)
        next_url = url_for('explore', page=predictions.next_num) if predictions.has_next else None
        prev_url = url_for('explore', page=predictions.prev_num) if predictions.has_prev else None
        return render_template('explore.html', title='Explore', form=form, predictions=predictions.items,
                               next_url=next_url, prev_url=prev_url)
    return render_template('explore.html', title='Explore')
