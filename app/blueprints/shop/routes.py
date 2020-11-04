from .import bp as shop
from flask import render_template, redirect, url_for, session, request, flash
from .models import Product


import stripe, os

@shop.route('/')
def get_products():
    context = {
        'products': Product.query.all(),
    }
    return render_template('marketplace.html', **context)


# @shop.route('/cart')
# def cart():
#     return render_template('cart.html')



stripe_keys = {
    'secret_key': os.getenv('STRIPE_SECRET_KEY'),
    'publishable_key': os.getenv('STRIPE_PUBLISHABLE_KEY')
}

stripe.api_key = stripe_keys['secret_key']

# @shop.route('/')
# def get_products():
#     context = {
#         'products': Product.query.all(),
#     }
#     return render_template('marketplace.html', **context)

@shop.route('/add')
def add_to_cart():
    print( request.args)
    _id = int(request.args.get('id'))
    p = Product.query.get(_id)
    item = {
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'image': p.image,
        'in_stock': p.in_stock,
        'description': p.description
    }
    # print("It works")
    session['cart']['items'].append(item)
    session['cart']['cart_total'] = 0
    for i in session['cart']['items']:
        session['cart']['cart_total'] += i['price']
    flash(f'{p.name} has been added to your cart', 'success')
    return redirect(url_for('shop.get_products'))

@shop.route('/remove')
def remove_from_cart():
    _id = int(request.args.get('id'))
    for item in session['cart']['items']:
        if _id == item['id']:
            session['cart']['items'].remove(item)
            # session['cart']['cart_total'] -= item['price']
            flash(f"Item has been removed", 'info')
            break
    return redirect(url_for('shop.cart'))

@shop.route('/clear')
def clear_cart():
    session['cart']['items'].clear()
    session['cart']['cart_total'] = 0
    flash('All items have been cleared from the cart.', 'danger')
    return redirect(url_for('shop.cart'))

@shop.route('/cart')
def cart():
    display_cart = []
    session['cart']['cart_total'] = 0
    for i in session['cart']['items']:
        if i not in display_cart:
            display_cart.append(i)
        session['cart']['cart_total'] += i['price']
    for i in display_cart:
        i['quantity'] =session['cart']['items'].count(i)
    session['display_cart'] = display_cart
    context = {
        'items': display_cart,
        'cart_total': session['cart']['cart_total'],
        'stripe_publishable_key': stripe_keys['publishable_key']
    }
    return render_template('cart.html', **context)

@shop.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    stripe_line_items = []
    for p in session['display_cart']:
        product_dict = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': p['name'],
                    'description': p['description'],
                    'images': [p['image']]
                },
                'unit_amount': int(p['price'] * 100),
            },
            'quantity': session['cart']['items'].count(p),
        }
        stripe_line_items.append(product_dict)
        # print(product_dict)
    # print(strip_line_items)
    stripe_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=stripe_line_items,
        mode='payment',
        success_url='http://localhost:5000/shop/checkout/success',
        cancel_url='http://localhost:5000/shop/checkout/cancel'
    )
    # Pass String session information to either the success/cancel routes
    session['stripe_Not a valid email addresssession_information'] = stripe_session

    # Clear all items from cart and reset cart_total to 0
    session['cart']['items'].clear()
    session['cart']['cart_total'] = 0

    # Return/Send the stripe session information back to cart.html
    return stripe_session

@shop.route('/checkout/success')
def checkout_success():
    print("Success")
    return render_template('checkout-success.html', stripe_session=session['stripe_session_information'])

@shop.route('/checkout/cancel')
def checkout_cancel():
    print("Unsucessful")
    return redirect(url_for('shop.cart'))



# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         r = request.form
#         if r.get('confirm_password') == r.get('password'):
#             data = {
#                 'first_name': r.get('first_name'),
#                 'last_name': r.get('last_name'),
#                 'email': r.get('email'),
#                 'password': r.get('password'),
#             }
#             u = User(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=data['password'])
#             u.hash_password(u.password)
#             db.session.add(u)
#             db.session.commit()
#             flash("You have registered successfully", 'primary')
#             return redirect(url_for('login'))
#     return render_template('register.html')
