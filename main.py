from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import random
import stripe
import os
import smtplib
import json
from flask_ckeditor import CKEditorField

APP_NAME = 'ENTER HERE'


app = Flask(__name__)
ckeditor = CKEditor(app)
Bootstrap5(app)
app.config['SECRET_KEY'] = '1afjdlkafjd'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", 'sqlite:///users.db')
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Create a form to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired() ])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")

# Create a form to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")

class ChangePassword(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    submit = SubmitField("Change Password")

class Feedback(FlaskForm):
    feedback = StringField("Feedback", validators=[DataRequired()])
    submit = SubmitField("Provide Feedback")

class NoteInput(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    subject = StringField("Subject", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()], render_kw={"rows": 10})
    submit = SubmitField("Save Notes")

#user DB
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    premium_level: Mapped[int] = mapped_column(Integer)

with app.app_context():
    db.create_all()

@app.route('/', methods=["GET", "POST"])
def home_page():
    return render_template("index.html")

@app.route('/quiz', methods=["GET", "POST"])
def quiz():
    with open('economics_quiz.json', 'r') as file:
        quiz = json.load(file)
    return render_template("quiz.html", quiz=quiz)

@app.route('/note-input', methods=["GET", "POST"])
def note_input():
    form = NoteInput()
    #need to add logic to save the note to the database
    #ensure data is saved to the database for the notes
    return render_template("note_input.html", form=form)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
            premium=0
        )
        db.session.add(new_user)
        db.session.commit()
        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("INSERT HERE"))
    return render_template("register.html", form=form, current_user=current_user)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('INSERT HERE'))

    return render_template("login.html", form=form, current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('INSERT HERE'))

#for test of Stripe
YOUR_DOMAIN = 'http://127.0.0.1:5002'
#for live of Stripe
DOMAIN2 = 'https://bingebuddy.us'

@app.route('/create-checkout-session', methods=['POST', 'GET'])
def create_checkout_session():
    try:
        # stripe.Coupon.create(
        # id="free-test",
        # percent_off=100,
        # )
        # stripe.PromotionCode.create(
        # coupon="free-test",
        # code="FREETEST",
        # )
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                'currency': 'usd',
                'product_data': {
                'name': 'Movie Access',},
                'unit_amount': 299,},
                'quantity': 1,}],
            mode='payment',
            allow_promotion_codes = True,
            success_url=DOMAIN2 + '/success',
            cancel_url=DOMAIN2 + '/cancel',)
    except Exception as e:
        return str(e)
    return redirect(checkout_session.url, code=303)

@app.route('/cancel', methods=['POST', 'GET'])
def cancel_session():
    return redirect(url_for('INSERT HERE'))

@app.route('/success', methods=['POST', 'GET'])
def success_session():
    with app.app_context():
        g_user = current_user.get_id()
        completed_update = db.session.execute(db.select(User).where(User.id == g_user)).scalar()
        completed_update.premium_level = 1
        db.session.commit()
    return redirect(url_for('INSERT HERE'))

@app.route('/privacy-policy', methods=['POST', 'GET'])
def privacy_policy():
    return render_template("privacy_policy.html")

@app.route('/terms-and-conditions', methods=['POST', 'GET'])
def terms_and_conditions():
    return render_template("terms_and_conditions.html")

@app.route('/change-password', methods=["GET", "POST"])
def change_password():
    form = ChangePassword()
    g_user = current_user.get_id()
    if form.validate_on_submit():
        password = form.password.data
        new_password = form.new_password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('change_password'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('change_password'))
        else:
            completed_update = db.session.execute(db.select(User).where(User.id == g_user)).scalar()
            completed_update.password = generate_password_hash(
                    new_password,
                    method='pbkdf2:sha256',
                    salt_length=8)
            db.session.commit()
            flash('Password Changed')
            return redirect(url_for('change_password'))

    return render_template("change_password.html", form=form, current_user=current_user)

@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    form=Feedback()
    if form.validate_on_submit():
        feedback = form.feedback.data
        my_email = os.environ.get('FROM_EMAIL')
        password = os.environ.get('EMAIL_PASS')
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, 
                            to_addrs=os.environ.get('TO_EMAIL'), 
                            msg=f"Subject:Feedback from {APP_NAME}!\n\nFeedback: {feedback}",
                            )
        connection.close()
        flash('Feedback received! Thank you for taking the time to help.')
    return render_template("feedback.html", form=form)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
