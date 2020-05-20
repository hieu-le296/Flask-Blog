# core/views.py

from flask_dance.contrib.google import make_google_blueprint, google
from flask import render_template, request, Blueprint, redirect, url_for
from socialblog.models import BlogPost
import stripe

core = Blueprint('core', __name__)

public_key = 'pk_test_TYooMQauvdEDq54NiTphI7jx'
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(
        BlogPost.date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', blog_posts=blog_posts)

@core.route('/info')
def info():
    return render_template('info.html')

@core.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


@core.route('/donation')
def donation():
    return render_template('donation.html', public_key=public_key)


@core.route('/donation', methods=['POST'])
def payment():
    # Customer Info
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'], source=request.form['stripeToken'])

    # Payment Information
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=199,
        currency="CAD",
        description='Donation'
    )
    return redirect(url_for('core.thankyou'))
