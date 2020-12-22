from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL
from wtforms.fields.html5 import DateField
from wtforms_sqlalchemy.fields import QuerySelectField
from .models import User, Races, participants, RunningStatistics


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=15)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    favorite_race = SelectField('Favorite Race', choices = [('5K', '5k'), 
      ('10K', '10k'), ('Half', 'half'), ('Marathon', 'marathon'), ('Ultra Marathon', 'ultra'), ('I\'m not a runner', '0')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    recaptcha = RecaptchaField()
    submit = SubmitField('Login')

  
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=15)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    favorite_race = SelectField('Favorite Race', choices = [('5K', '5k'), 
      ('10K', '10k'), ('Half', 'half'), ('Marathon', 'marathon'), ('Ultra Marathon', 'ultra'), ('I\'m not a runner', '0')])
    submit = SubmitField('Update')

    def validate_username(self, username):
      if username.data != current_user.username:
        user = User.query.filter_by(username=username).first()
        if user:
          raise ValidationError('That username is taken; please choose a different one!')

    def validate_email(self, email):
      if email.data != current_user.email:
        user = User.query.filter_by(email=email).first()
        if user:
          raise ValidationError('That email is taken; please choose a different one!')


class AddRaceForm(FlaskForm):
  race_name = StringField('Race Name', validators=[DataRequired(), Length(min=5, max=100)])
  race_type = SelectField('Race Type', choices = [('Road', 'Road'), 
      ('Ultra', 'Ultra'), ('OCR', 'OCR'), ('Triathlon', 'Triathlon'), ('Trail', 'Trail')])
  race_date = DateField('Race Date', format='%Y-%m-%d', validators=[DataRequired()])
  race_city = StringField('Race City', validators=[DataRequired(), Length(min=3, max=25)])
  race_state = StringField('Race State or Country', validators=[DataRequired(), Length(min=2, max=25)])
  race_url = StringField('Race Website', validators=[URL()])
  submit = SubmitField('Add Race')


class UpdateSecurityForm(FlaskForm):
  # existing_password = PasswordField('Existing Password', validators=[DataRequired()])
  new_password = PasswordField('New Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
  submit = SubmitField('Update Password')
  

def race_participant_query():
  return Races.query

class RaceParticipants(FlaskForm):
  runners_race = QuerySelectField(query_factory=race_participant_query, allow_blank=False, get_label='race_name')
  submit = SubmitField('Add Your Race!')


class RunningStatisticsForm(FlaskForm):
  mile_pr = StringField('Mile PR')
  fivek_pr = StringField('5K PR')
  tenk_pr = StringField('10K PR')
  half_pr = StringField('Half Marathon PR')
  marathon_pr = StringField('Marathon PR')
  fiftyk_pr = StringField('50K PR')
  hundredk_pr = StringField('100K PR')
  fiftym_pr = StringField('50M PR')
  hundredm_pr = StringField('100M PR')
  running_streak_pr = StringField('Running Streak PR')
  annual_miles_pr = StringField('Annual Miles PR')
  most_races_year = StringField('Most Races in a Year')
  submit = SubmitField('Add Your Numbers!')
