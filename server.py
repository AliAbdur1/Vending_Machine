from flask import Flask, render_template, request, redirect, url_for, session
# from session import Session

app = Flask(__name__)
app.secret_key = 'vendingmachine'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Backend using OOP
class Item:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

class VendingMachine:
    def __init__(self):
        self.items = [
            Item('Soda', 1.50, 10),
            Item('Chips', 1.00, 15),
            Item('Candy', 0.75, 20),
            Item('Gum', 0.50, 30),
            Item('Tooth Paste', 2.00, 10),
            Item('Baby butter', 7.00, 6)
        ]

    def get_items(self):
        return self.items

    def get_item(self, name):
        for item in self.items:
            if item.name == name:
                return item
        return None
    
    def restock_item(self, name, quantity):
        item = self.get_item(name)
        if item:
            item.quantity += quantity
            return item
        return None

vending_machine = VendingMachine()

@app.route('/')
def index():
    items = vending_machine.get_items()
    return render_template('index.html', items=items)

@app.route('/select_item/<name>', methods=['GET', 'POST'])
def select_item(name):
    item = vending_machine.get_item(name)
    if item:
        if request.method == 'POST':
            quantity = int(request.form.get('quantity'))
            cart = session.get('cart', [])
            cart.append({'name': item.name, 'price': item.price, 'quantity': quantity})
            session['cart'] = cart
            return redirect(url_for('view_cart'))
        return render_template('select_items.html', item=item)
    else:
        return redirect(url_for('page_not_found', e=404))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return render_template('checkout.html')

@app.route('/restock_item/<name>', methods=['GET', 'POST'])
def restock_item(name):
    item = vending_machine.get_item(name)
    if item:
        if request.method == 'POST':
            quantity = int(request.form.get('quantity'))
            vending_machine.restock_item(name, quantity)
            return redirect(url_for('index'))
        return render_template('restock_item.html', item=item)
    else:
        return redirect(url_for('page_not_found', e=404))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True)

