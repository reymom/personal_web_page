from datetime import datetime
from guess_language import guess_language

from flask import flash, g, redirect, render_template, request, url_for, jsonify
from flask_babel import _, get_locale
from flask_login import current_user, login_required
from app import current_app, db
from app.main import bp
from app.main.forms import EditProfileForm, PredictionForm, SearchForm
from app.models import User, Prediction
from app.translate import translate


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.las_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    predictions, total = Prediction.search(g.search_form.q.data, page, current_app.config['PREDICTIONS_PER_PAGE_USER'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['PREDICTIONS_PER_PAGE_USER'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), predictions=predictions, total=total,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/')
@bp.route('/index')
def index():
    if not current_user.is_anonymous:
        page = request.args.get('page', 1, type=int)
        predictions = current_user.followed_predictions().paginate(
            page, current_app.config['PREDICTIONS_PER_PAGE_INDEX'], False)
        next_url = url_for('main.index', page=predictions.next_num) if predictions.has_next else None
        prev_url = url_for('main.index', page=predictions.prev_num) if predictions.has_prev else None
        return render_template('index.html', title=_('Home'), predictions=predictions.items,
                                next_url=next_url, prev_url=prev_url)
    return render_template('index.html', title=_('Home'))


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    predictions = user.prediction_ids.order_by(Prediction.timestamp.desc()).paginate(
        page, current_app.config['PREDICTIONS_PER_PAGE_USER'], False)
    next_url = url_for('main.user', username=user.username, page=predictions.next_num) \
        if predictions.has_next else None
    prev_url = url_for('main.user', username=user.username, page=predictions.prev_num) \
        if predictions.has_prev else None
    return render_template('user.html', user=user, predictions=predictions.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'), form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot (un)follow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    form = PredictionForm()
    if form.validate_on_submit():
        language = guess_language(form.prediction.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        prediction = Prediction(
            body=form.prediction.data,
            author=current_user,
            language=language
        )
        db.session.add(prediction)
        db.session.commit()
        flash('Your prediction is now posted!')
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    predictions = Prediction.query.order_by(Prediction.timestamp.desc()).paginate(
        page, current_app.config['PREDICTIONS_PER_PAGE_INDEX'], False)
    next_url = url_for('main.explore', page=predictions.next_num) if predictions.has_next else None
    prev_url = url_for('main.explore', page=predictions.prev_num) if predictions.has_prev else None
    return render_template('explore.html', title=_('Explore'), form=form, predictions=predictions.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({
        'text': translate(request.form['text'], request.form['source_language'], request.form['dest_language'])
    })
