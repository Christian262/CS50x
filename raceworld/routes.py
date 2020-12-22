from flask import Flask, redirect, render_template, request, url_for,flash
from raceworld import app, db, bcrypt
from .forms import (RegistrationForm, LoginForm, UpdateAccountForm, AddRaceForm, 
                    UpdateSecurityForm, RaceParticipants, RunningStatisticsForm)
from .models import User, Races, RunningStatistics
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/races")
@app.route("/races/")
def races():

    races = Races.query.order_by(Races.race_date.asc())

    return render_template("races.html", races=races)


@app.route("/runners/")
@app.route("/runners")
def runners():

    users = User.query.order_by(User.date_registered.desc()).limit(5).all()

    return render_template("runners.html", users=users)


@app.route('/runners/<string:username>')
def runner(username):

    user = User.query.filter_by(username=username).first()

    return render_template('runner.html', user=user)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    existing_user = User.query.filter_by(email=form.email.data).first()
    if existing_user is None:
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, 
                    password=hashed_password, favorite_race=form.favorite_race.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Email or password incorrect', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

# Update Runner Account Info
@app.route("/runners/<string:username>/update-account", methods=["GET", "POST"])
@login_required
def update_runner(username):
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.favorite_race = form.favorite_race.data
        db.session.commit()
        flash('Your account has been successfully updated!', 'success')
        return render_template('update_runner.html', form=form)
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.favorite_race.data = current_user.favorite_race
    return render_template('update_runner.html', form=form)


# Update Password
@app.route("/runners/<string:username>/update-password", methods=["GET", "POST"])
@login_required
def update_security(username):
    form = UpdateSecurityForm()
        # password = User.query.filter_by(existing_password=form.existing_password.data).first()
    if form.validate_on_submit():
        # if form.existing_password != current_user.password:
        #     flash('The password is incorrect!', 'danger')
        #     return render_template('update_security.html', form=form)
        # else:
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        logout_user()
        return redirect(url_for('login'))
    return render_template('update_security.html', form=form)


#Add Race
@app.route("/races/add", methods=['GET', 'POST'])
@login_required
def add_race():
    form = AddRaceForm()
    existing_race = Races.query.filter_by(race_name=form.race_name.data).first()
    if existing_race is None:
        if form.validate_on_submit():
            race = Races(race_name=form.race_name.data, race_type=form.race_type.data, race_date=form.race_date.data,
                        race_city=form.race_city.data, race_state=form.race_state.data, race_url=form.race_url.data)
            db.session.add(race)
            db.session.commit()
            flash(f'Successfully added {form.race_name.data}!', 'success')
            return redirect(url_for('races'))
        return render_template('add_race.html', form=form)


#Add User to Races
@app.route("/runners/<string:username>/add-registered-race", methods=['GET', 'POST'])
@login_required
def add_registered_race(username):
    form = RaceParticipants()
    if form.validate_on_submit():
        race = form.runners_race.data
        current_user.races.append(race)
        db.session.commit()
        return redirect(url_for('runner',username=current_user.username))
    return render_template('add_registered_race.html', form=form)


@app.route("/runners/<string:username>/add-running-stats", methods=['GET', 'POST'])
@login_required
def running_stats(username):
    form = RunningStatisticsForm()
    if form.validate_on_submit():
        stats = RunningStatistics(
            mile_pr=form.mile_pr.data,
            fivek_pr=form.fivek_pr.data,
            tenk_pr=form.tenk_pr.data,
            half_pr=form.half_pr.data,
            marathon_pr=form.marathon_pr.data,
            fiftyk_pr=form.fiftyk_pr.data,
            hundredk_pr=form.hundredk_pr.data,
            fiftym_pr=form.fiftym_pr.data,
            hundredm_pr=form.hundredm_pr.data,
            running_streak_pr=form.running_streak_pr.data,
            annual_miles_pr=form.annual_miles_pr.data,
            most_races_year=form.most_races_year.data,
            user_id=current_user.id
            )
        db.session.add(stats)
        db.session.commit()
        flash(f'Stats updated for {current_user.username}!', 'success')
        return redirect(url_for('runner', username=current_user.username))
    return render_template('add_running_stats.html', form=form)


@app.route("/runners/<string:username>/update-running-stats", methods=['GET', 'POST'])
@login_required
def update_running_stats(username):
    form = RunningStatisticsForm()
    if form.validate_on_submit():
        current_user.running_stats.mile_pr=form.mile_pr.data
        current_user.running_stats.fivek_pr=form.fivek_pr.data
        current_user.running_stats.tenk_pr=form.tenk_pr.data
        current_user.running_stats.half_pr=form.half_pr.data
        current_user.running_stats.marathon_pr=form.marathon_pr.data
        current_user.running_stats.fiftyk_pr=form.fiftyk_pr.data
        current_user.running_stats.hundredk_pr=form.hundredk_pr.data
        current_user.running_stats.fiftym_pr=form.fiftym_pr.data
        current_user.running_stats.hundredm_pr=form.hundredm_pr.data
        current_user.running_stats.running_streak_pr=form.running_streak_pr.data
        current_user.running_stats.annual_miles_pr=form.annual_miles_pr.data
        current_user.running_stats.most_races_year=form.most_races_year.data
        # user_id=current_user.id
        db.session.commit()
        flash(f'Stats updated for {current_user.username}!', 'success')
        return redirect(url_for('runner', username=current_user.username))
    elif request.method == 'GET':
        form.mile_pr.data=current_user.running_stats.mile_pr
        form.fivek_pr.data=current_user.running_stats.fivek_pr
        form.tenk_pr.data=current_user.running_stats.tenk_pr
        form.half_pr.data=current_user.running_stats.half_pr
        form.marathon_pr.data=current_user.running_stats.marathon_pr
        form.fiftyk_pr.data=current_user.running_stats.fiftyk_pr
        form.hundredk_pr.data=current_user.running_stats.hundredk_pr
        form.fiftym_pr.data=current_user.running_stats.fiftym_pr
        form.hundredm_pr.data=current_user.running_stats.hundredm_pr
        form.running_streak_pr.data=current_user.running_stats.running_streak_pr
        form.annual_miles_pr.data=current_user.running_stats.annual_miles_pr
        form.most_races_year.data=current_user.running_stats.most_races_year
    return render_template('add_running_stats.html', form=form)


@app.errorhandler(404)
def error404(error):
    return render_template('404.html'), 404


@app.errorhandler(405)
def error405(error):
    return render_template('405.html'), 405


@app.errorhandler(500)
def error500(error):
    return render_template('500.html'), 500