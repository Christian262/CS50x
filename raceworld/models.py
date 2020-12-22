from datetime import datetime
from raceworld import db, app, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


participants = db.Table('participants',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('races_id', db.Integer, db.ForeignKey('races.id'))
    )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    favorite_race = db.Column(db.String(30), nullable=False)
    racer = db.relationship('Races', secondary=participants, backref=db.backref('racers'))
    running_stats = db.relationship('RunningStatistics', backref='user', uselist=False, lazy=True)


    def __repr__(self):
        return (f"User('{self.username}', '{self.password}', '{self.date_registered}', '{self.email}', '{self.favorite_race}')")


class Races(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    race_name = db.Column(db.String(100), unique=True, nullable=False)
    race_type = db.Column(db.String(30), nullable=False)
    race_date = db.Column(db.String(30))
    race_city = db.Column(db.String(25), nullable=False)
    race_state = db.Column(db.String(25), nullable=False)
    race_date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    race_url = db.Column(db.String(100), unique=True)
    races = db.relationship('User', secondary=participants, backref=db.backref('races'))


    def __repr__(self):
        return (f"('{self.race_name}',)")


class RunningStatistics(db.Model):
    __tablename__ = 'runningstatistics'
    id = db.Column(db.Integer, primary_key=True)
    mile_pr = db.Column(db.String(10))
    fivek_pr = db.Column(db.String(10))
    tenk_pr = db.Column(db.String(10))
    half_pr = db.Column(db.String(10))
    marathon_pr = db.Column(db.String(10))
    fiftyk_pr = db.Column(db.String(10))
    hundredk_pr = db.Column(db.String(10))
    fiftym_pr = db.Column(db.String(10))
    hundredm_pr = db.Column(db.String(10))
    running_streak_pr = db.Column(db.Integer)
    annual_miles_pr = db.Column(db.Integer)
    most_races_year = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False,  unique=True)
       
    def __repr__(self):
        return (f"RunningStats('{self.fivek_pr}', '{self.half_pr}', '{self.marathon_pr}')")
